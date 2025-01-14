from flask import session
from sqlalchemy.sql import text
from db import db

def get_post(id):
    sql = text("SELECT id, topic_id, user_id, content, created_at FROM posts WHERE id=:id")
    result = db.session.execute(sql, {"id": id})
    return result.fetchone()

def get_posts(topic_id):
    sql = text("SELECT id, topic_id, user_id, content, created_at FROM posts WHERE topic_id=:topic_id")
    result = db.session.execute(sql, {"topic_id": topic_id})
    return result.fetchall()

def get_post_count(topic_id):
    sql = text("SELECT COUNT(*) FROM posts WHERE topic_id=:topic_id")
    result = db.session.execute(sql, {"topic_id": topic_id})
    return result.fetchone()[0]

def create_post(topic_id, content):
    try:
        user_id = session.get("user_id")
        if not user_id:
            raise Exception("User not logged in")

        sql = text("""
            INSERT INTO posts (topic_id, user_id, content)
            VALUES (:topic_id, :user_id, :content)
        """)

        db.session.execute(sql, {"topic_id": topic_id, "user_id": user_id, "content": content})
        db.session.commit()
        return True
    except Exception as e:
        print("Error creating post:", e)
        return False
