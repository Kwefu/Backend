from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey, Enum, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime
import os
import enum

# Configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./forum.db")
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

# Association table for followers (many-to-many)
followers_table = Table(
    'followers',
    Base.metadata,
    Column('follower_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('following_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('created_at', DateTime, default=datetime.utcnow)
)

# Database Models
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    avatar_url = Column(String(255))
    bio = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    posts = relationship("Post", back_populates="author", cascade="all, delete-orphan")
    comments = relationship("Comment", back_populates="author", cascade="all, delete-orphan")
    likes = relationship("Like", back_populates="user", cascade="all, delete-orphan")
    votes = relationship("Vote", back_populates="user", cascade="all, delete-orphan")
    status_updates = relationship("StatusUpdate", back_populates="user", cascade="all, delete-orphan")
    
    # Followers/Following relationships
    followers = relationship(
        "User",
        secondary=followers_table,
        primaryjoin=id == followers_table.c.following_id,
        secondaryjoin=id == followers_table.c.follower_id,
        backref="following"
    )

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
    votes = relationship("Vote", back_populates="post", cascade="all, delete-orphan")

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

class Vote(Base):
    __tablename__ = "votes"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)
    vote_type = Column(String(10))  # 'upvote' or 'downvote'
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="votes")
    post = relationship("Post", back_populates="votes")

class StatusUpdate(Base):
    __tablename__ = "status_updates"
    
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="status_updates")

# Create tables
try:
    Base.metadata.create_all(bind=engine)
except Exception as e:
    print(f"Database initialization error: {e}")

# Pydantic Schemas
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    bio: Optional[str] = None

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    bio: Optional[str] = None
    avatar_url: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    avatar_url: Optional[str]
    bio: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True

class UserProfileResponse(BaseModel):
    id: int
    username: str
    email: str
    avatar_url: Optional[str]
    bio: Optional[str]
    created_at: datetime
    followers_count: int
    following_count: int
    posts_count: int
    
    class Config:
        from_attributes = True

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
        from_attributes = True

class PostCreate(BaseModel):
    title: Optional[str]
    content: str
    forum_id: int
    image_url: Optional[str]
    user_id: int

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
    votes_count: int
    
    class Config:
        from_attributes = True

class CommentCreate(BaseModel):
    content: str
    post_id: int
    user_id: int

class CommentResponse(BaseModel):
    id: int
    content: str
    author: UserResponse
    post_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class LikeCreate(BaseModel):
    post_id: int
    user_id: int

class VoteCreate(BaseModel):
    post_id: int
    user_id: int
    vote_type: str  # 'upvote' or 'downvote'

class StatusUpdateCreate(BaseModel):
    content: str
    user_id: int

class StatusUpdateResponse(BaseModel):
    id: int
    content: str
    user: UserResponse
    created_at: datetime
    
    class Config:
        from_attributes = True

class FollowCreate(BaseModel):
    follower_id: int
    following_id: int

# FastAPI App
app = FastAPI(title="Forum API - Profile Extended", version="2.0.0")

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

# ============ USER & PROFILE ENDPOINTS ============

@app.get("/")
def root():
    return {
        "message": "Forum API with Profile Features",
        "docs": "/docs"
    }

@app.post("/api/users", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """Tạo user mới"""
    existing = db.query(User).filter(User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already exists")
    
    existing_username = db.query(User).filter(User.username == user.username).first()
    if existing_username:
        raise HTTPException(status_code=400, detail="Username already taken")
    
    new_user = User(
        username=user.username,
        email=user.email,
        bio=user.bio
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get("/api/users", response_model=List[UserResponse])
def get_users(db: Session = Depends(get_db)):
    """Lấy danh sách users"""
    users = db.query(User).all()
    return users

@app.get("/api/users/{user_id}", response_model=UserProfileResponse)
def get_user_profile(user_id: int, db: Session = Depends(get_db)):
    """Lấy profile đầy đủ của user"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return UserProfileResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        avatar_url=user.avatar_url,
        bio=user.bio,
        created_at=user.created_at,
        followers_count=len(user.followers),
        following_count=len(user.following),
        posts_count=len(user.posts)
    )

@app.put("/api/users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    """Cập nhật thông tin user"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user_update.username:
        user.username = user_update.username
    if user_update.email:
        user.email = user_update.email
    if user_update.bio is not None:
        user.bio = user_update.bio
    if user_update.avatar_url is not None:
        user.avatar_url = user_update.avatar_url
    
    db.commit()
    db.refresh(user)
    return user

@app.get("/api/users/{user_id}/posts", response_model=List[PostResponse])
def get_user_posts(user_id: int, skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    """Lấy tất cả posts của user"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    posts = db.query(Post).filter(Post.author_id == user_id).order_by(Post.created_at.desc()).offset(skip).limit(limit).all()
    
    return [PostResponse(
        id=p.id,
        title=p.title,
        content=p.content,
        image_url=p.image_url,
        author=p.author,
        forum_id=p.forum_id,
        created_at=p.created_at,
        likes_count=len(p.likes),
        comments_count=len(p.comments),
        votes_count=len([v for v in p.votes if v.vote_type == 'upvote']) - len([v for v in p.votes if v.vote_type == 'downvote'])
    ) for p in posts]

@app.get("/api/users/{user_id}/activity", response_model=List[PostResponse])
def get_user_activity(user_id: int, skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    """Lấy hoạt động gần đây của user (posts + comments)"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Lấy posts mà user đã comment
    commented_posts = db.query(Post).join(Comment).filter(Comment.author_id == user_id).order_by(Comment.created_at.desc()).offset(skip).limit(limit).all()
    
    return [PostResponse(
        id=p.id,
        title=p.title,
        content=p.content,
        image_url=p.image_url,
        author=p.author,
        forum_id=p.forum_id,
        created_at=p.created_at,
        likes_count=len(p.likes),
        comments_count=len(p.comments),
        votes_count=len([v for v in p.votes if v.vote_type == 'upvote']) - len([v for v in p.votes if v.vote_type == 'downvote'])
    ) for p in commented_posts]

# ============ FOLLOW/UNFOLLOW ENDPOINTS ============

@app.post("/api/follow")
def follow_user(follow: FollowCreate, db: Session = Depends(get_db)):
    """Follow một user"""
    follower = db.query(User).filter(User.id == follow.follower_id).first()
    following = db.query(User).filter(User.id == follow.following_id).first()
    
    if not follower or not following:
        raise HTTPException(status_code=404, detail="User not found")
    
    if follow.follower_id == follow.following_id:
        raise HTTPException(status_code=400, detail="Cannot follow yourself")
    
    # Check if already following
    if following in follower.following:
        raise HTTPException(status_code=400, detail="Already following this user")
    
    follower.following.append(following)
    db.commit()
    
    return {"message": "Followed successfully"}

@app.post("/api/unfollow")
def unfollow_user(follow: FollowCreate, db: Session = Depends(get_db)):
    """Unfollow một user"""
    follower = db.query(User).filter(User.id == follow.follower_id).first()
    following = db.query(User).filter(User.id == follow.following_id).first()
    
    if not follower or not following:
        raise HTTPException(status_code=404, detail="User not found")
    
    if following not in follower.following:
        raise HTTPException(status_code=400, detail="Not following this user")
    
    follower.following.remove(following)
    db.commit()
    
    return {"message": "Unfollowed successfully"}

@app.get("/api/users/{user_id}/followers", response_model=List[UserResponse])
def get_followers(user_id: int, db: Session = Depends(get_db)):
    """Lấy danh sách followers"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user.followers

@app.get("/api/users/{user_id}/following", response_model=List[UserResponse])
def get_following(user_id: int, db: Session = Depends(get_db)):
    """Lấy danh sách following"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user.following

# ============ STATUS UPDATE ENDPOINTS ============

@app.post("/api/status", response_model=StatusUpdateResponse)
def create_status_update(status: StatusUpdateCreate, db: Session = Depends(get_db)):
    """Tạo status update mới"""
    user = db.query(User).filter(User.id == status.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    new_status = StatusUpdate(
        content=status.content,
        user_id=status.user_id
    )
    db.add(new_status)
    db.commit()
    db.refresh(new_status)
    return new_status

@app.get("/api/users/{user_id}/status", response_model=List[StatusUpdateResponse])
def get_user_status_updates(user_id: int, limit: int = 10, db: Session = Depends(get_db)):
    """Lấy status updates của user"""
    statuses = db.query(StatusUpdate).filter(StatusUpdate.user_id == user_id).order_by(StatusUpdate.created_at.desc()).limit(limit).all()
    return statuses

# ============ VOTE ENDPOINTS ============

@app.post("/api/votes")
def create_vote(vote: VoteCreate, db: Session = Depends(get_db)):
    """Vote (upvote/downvote) một post"""
    user = db.query(User).filter(User.id == vote.user_id).first()
    post = db.query(Post).filter(Post.id == vote.post_id).first()
    
    if not user or not post:
        raise HTTPException(status_code=404, detail="User or Post not found")
    
    if vote.vote_type not in ['upvote', 'downvote']:
        raise HTTPException(status_code=400, detail="Invalid vote type")
    
    # Check if already voted
    existing_vote = db.query(Vote).filter(Vote.user_id == vote.user_id, Vote.post_id == vote.post_id).first()
    
    if existing_vote:
        if existing_vote.vote_type == vote.vote_type:
            # Remove vote if same type
            db.delete(existing_vote)
            db.commit()
            return {"message": "Vote removed"}
        else:
            # Change vote type
            existing_vote.vote_type = vote.vote_type
            db.commit()
            return {"message": f"Vote changed to {vote.vote_type}"}
    
    new_vote = Vote(
        user_id=vote.user_id,
        post_id=vote.post_id,
        vote_type=vote.vote_type
    )
    db.add(new_vote)
    db.commit()
    return {"message": f"{vote.vote_type} successful"}

@app.get("/api/posts/{post_id}/votes")
def get_post_votes(post_id: int, db: Session = Depends(get_db)):
    """Lấy số votes của post"""
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    upvotes = len([v for v in post.votes if v.vote_type == 'upvote'])
    downvotes = len([v for v in post.votes if v.vote_type == 'downvote'])
    
    return {
        "upvotes": upvotes,
        "downvotes": downvotes,
        "total": upvotes - downvotes
    }

# ============ EXISTING ENDPOINTS (from previous code) ============

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
    """Lấy danh sách forums"""
    query = db.query(Forum)
    if category:
        query = query.filter(Forum.category == category)
    return query.all()

@app.post("/api/posts", response_model=PostResponse)
def create_post(post: PostCreate, db: Session = Depends(get_db)):
    """Tạo post mới"""
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
    
    return PostResponse(
        id=new_post.id,
        title=new_post.title,
        content=new_post.content,
        image_url=new_post.image_url,
        author=new_post.author,
        forum_id=new_post.forum_id,
        created_at=new_post.created_at,
        likes_count=len(new_post.likes),
        comments_count=len(new_post.comments),
        votes_count=0
    )

@app.get("/api/posts", response_model=List[PostResponse])
def get_posts(forum_id: Optional[int] = None, skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    """Lấy danh sách posts"""
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
        comments_count=len(p.comments),
        votes_count=len([v for v in p.votes if v.vote_type == 'upvote']) - len([v for v in p.votes if v.vote_type == 'downvote'])
    ) for p in posts]

@app.post("/api/likes")
def toggle_like(like: LikeCreate, db: Session = Depends(get_db)):
    """Like/Unlike post"""
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
    """Tạo comment"""
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
    """Lấy comments của post"""
    comments = db.query(Comment).filter(Comment.post_id == post_id).order_by(Comment.created_at.desc()).all()
    return comments

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)