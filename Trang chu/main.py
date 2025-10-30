from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime
import enum
import os

# Configuration: use env var or fall back to local sqlite for dev
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./forum.db")

# For sqlite we must pass check_same_thread
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

# Database Setup
engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Enums
class CategoryEnum(str, enum.Enum):
    GAME = "game"
    SPORT = "the_thao"
    BUSINESS = "kinh_doanh"
    MOVIE = "phim"
    ART = "nghe_thuat"

# Database Models
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    avatar_url = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    posts = relationship("Post", back_populates="author", cascade="all, delete-orphan")
    comments = relationship("Comment", back_populates="author", cascade="all, delete-orphan")
    likes = relationship("Like", back_populates="user", cascade="all, delete-orphan")

class Forum(Base):
    __tablename__ = "forums"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
    category = Column(Enum(CategoryEnum), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    created_by = Column(Integer, ForeignKey("users.id"))
    
    posts = relationship("Post", back_populates="forum", cascade="all, delete-orphan")

class Post(Base):
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255))
    content = Column(Text, nullable=False)
    image_url = Column(String(255))
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    forum_id = Column(Integer, ForeignKey("forums.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    author = relationship("User", back_populates="posts")
    forum = relationship("Forum", back_populates="posts")
    comments = relationship("Comment", back_populates="post", cascade="all, delete-orphan")
    likes = relationship("Like", back_populates="post", cascade="all, delete-orphan")

class Comment(Base):
    __tablename__ = "comments"
    
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    author = relationship("User", back_populates="comments")
    post = relationship("Post", back_populates="comments")

class Like(Base):
    __tablename__ = "likes"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="likes")
    post = relationship("Post", back_populates="likes")

# Create tables (don't crash server if DB not available at startup)
try:
    Base.metadata.create_all(bind=engine)
except Exception as e:
    print("Warning: could not create DB tables on startup:", e)

# Pydantic Schemas
class UserCreate(BaseModel):
    username: str
    email: EmailStr

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    avatar_url: Optional[str]
    created_at: datetime
    
    class Config:
        orm_mode = True

class ForumCreate(BaseModel):
    name: str
    description: Optional[str]
    category: CategoryEnum

class ForumResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    category: CategoryEnum
    created_at: datetime
    
    class Config:
        orm_mode = True

class PostCreate(BaseModel):
    title: Optional[str]
    content: str
    forum_id: int
    image_url: Optional[str]
    user_id: int  # Giờ phải truyền user_id trực tiếp

class PostResponse(BaseModel):
    id: int
    title: Optional[str]
    content: str
    image_url: Optional[str]
    author: UserResponse
    forum_id: int
    created_at: datetime
    likes_count: int
    comments_count: int
    
    class Config:
        orm_mode = True

class CommentCreate(BaseModel):
    content: str
    post_id: int
    user_id: int  # Phải truyền user_id

class CommentResponse(BaseModel):
    id: int
    content: str
    author: UserResponse
    post_id: int
    created_at: datetime
    
    class Config:
        orm_mode = True

class LikeCreate(BaseModel):
    post_id: int
    user_id: int  # Phải truyền user_id

# FastAPI App
app = FastAPI(title="Forum API - No Auth Version", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Helper function to create default user if needed
def get_or_create_default_user(db: Session):
    user = db.query(User).filter(User.id == 1).first()
    if not user:
        user = User(
            username="default_user",
            email="default@example.com"
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    return user

# Endpoints
@app.get("/")
def root():
    return {
        "message": "Forum API - No Authentication Version", 
        "warning": "⚠️ This is for TESTING ONLY. Do not use in production!",
        "docs": "/docs"
    }

@app.post("/api/users", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """Tạo user mới - KHÔNG CẦN PASSWORD"""
    existing = db.query(User).filter(User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already exists")
    
    existing_username = db.query(User).filter(User.username == user.username).first()
    if existing_username:
        raise HTTPException(status_code=400, detail="Username already taken")
    
    new_user = User(
        username=user.username,
        email=user.email
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get("/api/users", response_model=List[UserResponse])
def get_users(db: Session = Depends(get_db)):
    """Lấy danh sách tất cả users"""
    users = db.query(User).all()
    return users

@app.get("/api/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """Lấy thông tin 1 user"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.post("/api/forums", response_model=ForumResponse)
def create_forum(forum: ForumCreate, user_id: int = 1, db: Session = Depends(get_db)):
    """Tạo forum mới"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    new_forum = Forum(
        name=forum.name,
        description=forum.description,
        category=forum.category,
        created_by=user_id
    )
    db.add(new_forum)
    db.commit()
    db.refresh(new_forum)
    return new_forum

@app.get("/api/forums", response_model=List[ForumResponse])
def get_forums(category: Optional[CategoryEnum] = None, db: Session = Depends(get_db)):
    """Lấy danh sách forums, có thể filter theo category"""
    query = db.query(Forum)
    if category:
        query = query.filter(Forum.category == category)
    return query.all()

@app.get("/api/forums/{forum_id}", response_model=ForumResponse)
def get_forum(forum_id: int, db: Session = Depends(get_db)):
    """Lấy chi tiết 1 forum"""
    forum = db.query(Forum).filter(Forum.id == forum_id).first()
    if not forum:
        raise HTTPException(status_code=404, detail="Forum not found")
    return forum

@app.post("/api/posts", response_model=PostResponse)
def create_post(post: PostCreate, db: Session = Depends(get_db)):
    """Tạo bài post mới - CẦN TRUYỀN user_id"""
    user = db.query(User).filter(User.id == post.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    forum = db.query(Forum).filter(Forum.id == post.forum_id).first()
    if not forum:
        raise HTTPException(status_code=404, detail="Forum not found")
    
    new_post = Post(
        title=post.title,
        content=post.content,
        image_url=post.image_url,
        author_id=post.user_id,
        forum_id=post.forum_id
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    response = PostResponse(
        id=new_post.id,
        title=new_post.title,
        content=new_post.content,
        image_url=new_post.image_url,
        author=new_post.author,
        forum_id=new_post.forum_id,
        created_at=new_post.created_at,
        likes_count=len(new_post.likes),
        comments_count=len(new_post.comments)
    )
    return response

@app.get("/api/posts", response_model=List[PostResponse])
def get_posts(forum_id: Optional[int] = None, skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    """Lấy danh sách posts với pagination"""
    query = db.query(Post)
    if forum_id:
        query = query.filter(Post.forum_id == forum_id)
    posts = query.order_by(Post.created_at.desc()).offset(skip).limit(limit).all()
    
    return [PostResponse(
        id=p.id,
        title=p.title,
        content=p.content,
        image_url=p.image_url,
        author=p.author,
        forum_id=p.forum_id,
        created_at=p.created_at,
        likes_count=len(p.likes),
        comments_count=len(p.comments)
    ) for p in posts]

@app.get("/api/posts/{post_id}", response_model=PostResponse)
def get_post(post_id: int, db: Session = Depends(get_db)):
    """Lấy chi tiết 1 post"""
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    return PostResponse(
        id=post.id,
        title=post.title,
        content=post.content,
        image_url=post.image_url,
        author=post.author,
        forum_id=post.forum_id,
        created_at=post.created_at,
        likes_count=len(post.likes),
        comments_count=len(post.comments)
    )

@app.post("/api/likes")
def toggle_like(like: LikeCreate, db: Session = Depends(get_db)):
    """Like/Unlike một post - CẦN TRUYỀN user_id"""
    user = db.query(User).filter(User.id == like.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    post = db.query(Post).filter(Post.id == like.post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    existing_like = db.query(Like).filter(
        Like.user_id == like.user_id, 
        Like.post_id == like.post_id
    ).first()
    
    if existing_like:
        db.delete(existing_like)
        db.commit()
        return {"message": "Unlike successful", "liked": False}
    
    new_like = Like(user_id=like.user_id, post_id=like.post_id)
    db.add(new_like)
    db.commit()
    return {"message": "Like successful", "liked": True}

@app.post("/api/comments", response_model=CommentResponse)
def create_comment(comment: CommentCreate, db: Session = Depends(get_db)):
    """Tạo comment - CẦN TRUYỀN user_id"""
    user = db.query(User).filter(User.id == comment.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    post = db.query(Post).filter(Post.id == comment.post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    new_comment = Comment(
        content=comment.content,
        author_id=comment.user_id,
        post_id=comment.post_id
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment

@app.get("/api/posts/{post_id}/comments", response_model=List[CommentResponse])
def get_comments(post_id: int, db: Session = Depends(get_db)):
    """Lấy tất cả comments của 1 post"""
    comments = db.query(Comment).filter(Comment.post_id == post_id).order_by(Comment.created_at.desc()).all()
    return comments

@app.delete("/api/posts/{post_id}")
def delete_post(post_id: int, user_id: int, db: Session = Depends(get_db)):
    """Xóa post - CẦN TRUYỀN user_id để kiểm tra quyền"""
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    # Vẫn kiểm tra xem có phải author không
    if post.author_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this post")
    
    db.delete(post)
    db.commit()
    return {"message": "Post deleted successfully"}

@app.delete("/api/comments/{comment_id}")
def delete_comment(comment_id: int, user_id: int, db: Session = Depends(get_db)):
    """Xóa comment"""
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    
    if comment.author_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    db.delete(comment)
    db.commit()
    return {"message": "Comment deleted successfully"}

@app.get("/api/trending/posts", response_model=List[PostResponse])
def get_trending_posts(limit: int = 10, db: Session = Depends(get_db)):
    """Lấy các bài post trending (mới nhất)"""
    posts = db.query(Post).order_by(Post.created_at.desc()).limit(limit).all()
    return [PostResponse(
        id=p.id,
        title=p.title,
        content=p.content,
        image_url=p.image_url,
        author=p.author,
        forum_id=p.forum_id,
        created_at=p.created_at,
        likes_count=len(p.likes),
        comments_count=len(p.comments)
    ) for p in posts]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)