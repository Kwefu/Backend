"""
Script để import dữ liệu từ file JSON vào database
Chạy file này sau khi đã setup database
"""

import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Import models từ file main
from main import Base, User, Forum, Post, Comment, Like

# Database configuration
DATABASE_URL = "postgresql://user:password@localhost:5432/forum_db"

def load_json_data(filename="sample_data.json"):
    """Đọc dữ liệu từ file JSON"""
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

def import_data():
    """Import tất cả dữ liệu vào database"""
    
    # Tạo engine và session
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        # Đọc dữ liệu từ JSON
        data = load_json_data()
        
        print("🚀 Bắt đầu import dữ liệu...")
        
        # 1. Import Users
        print("\n👤 Importing users...")
        for user_data in data['users']:
            user = User(
                id=user_data['id'],
                username=user_data['username'],
                email=user_data['email'],
                avatar_url=user_data.get('avatar_url'),
                created_at=datetime.utcnow()
            )
            db.add(user)
        db.commit()
        print(f"✅ Imported {len(data['users'])} users")
        
        # 2. Import Forums
        print("\n📁 Importing forums...")
        for forum_data in data['forums']:
            forum = Forum(
                id=forum_data['id'],
                name=forum_data['name'],
                description=forum_data.get('description'),
                category=forum_data['category'],
                created_by=forum_data['created_by'],
                created_at=datetime.utcnow()
            )
            db.add(forum)
        db.commit()
        print(f"✅ Imported {len(data['forums'])} forums")
        
        # 3. Import Posts
        print("\n📝 Importing posts...")
        for post_data in data['posts']:
            post = Post(
                id=post_data['id'],
                title=post_data.get('title'),
                content=post_data['content'],
                image_url=post_data.get('image_url'),
                author_id=post_data['author_id'],
                forum_id=post_data['forum_id'],
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            db.add(post)
        db.commit()
        print(f"✅ Imported {len(data['posts'])} posts")
        
        # 4. Import Comments
        print("\n💬 Importing comments...")
        for comment_data in data['comments']:
            comment = Comment(
                content=comment_data['content'],
                author_id=comment_data['author_id'],
                post_id=comment_data['post_id'],
                created_at=datetime.utcnow()
            )
            db.add(comment)
        db.commit()
        print(f"✅ Imported {len(data['comments'])} comments")
        
        # 5. Import Likes
        print("\n❤️ Importing likes...")
        for like_data in data['likes']:
            like = Like(
                user_id=like_data['user_id'],
                post_id=like_data['post_id'],
                created_at=datetime.utcnow()
            )
            db.add(like)
        db.commit()
        print(f"✅ Imported {len(data['likes'])} likes")
        
        print("\n🎉 Import hoàn tất!")
        print("\n📊 Tổng kết:")
        print(f"   - Users: {len(data['users'])}")
        print(f"   - Forums: {len(data['forums'])}")
        print(f"   - Posts: {len(data['posts'])}")
        print(f"   - Comments: {len(data['comments'])}")
        print(f"   - Likes: {len(data['likes'])}")
        
    except Exception as e:
        print(f"\n❌ Lỗi: {e}")
        db.rollback()
    finally:
        db.close()

def clear_all_data():
    """Xóa toàn bộ dữ liệu (dùng khi cần reset)"""
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        print("🗑️ Đang xóa dữ liệu cũ...")
        db.query(Like).delete()
        db.query(Comment).delete()
        db.query(Post).delete()
        db.query(Forum).delete()
        db.query(User).delete()
        db.commit()
        print("✅ Đã xóa toàn bộ dữ liệu cũ")
    except Exception as e:
        print(f"❌ Lỗi khi xóa: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--clear":
        # Chạy: python import_data.py --clear
        confirm = input("⚠️ Bạn có chắc muốn xóa TOÀN BỘ dữ liệu? (yes/no): ")
        if confirm.lower() == "yes":
            clear_all_data()
            print("\nNhấn Enter để import dữ liệu mới hoặc Ctrl+C để thoát...")
            input()
            import_data()
        else:
            print("Đã hủy.")
    else:
        # Chạy: python import_data.py
        import_data()