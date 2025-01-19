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

def get_user_posts():
    user_id = session.get("user_id")
    if not user_id:
        return []

    sql = text("""
        SELECT posts.id, topic_id, posts.content, posts.created_at, topics.title AS topic_title
        FROM posts
        JOIN topics ON posts.topic_id = topics.id
        WHERE posts.user_id = :user_id
        ORDER BY posts.created_at DESC
    """)
    result = db.session.execute(sql, {"user_id": user_id})
    posts = result.fetchall()

    return posts

def delite_post(id):
    try:
        user_id = session.get("user_id")
        if not user_id:
            raise Exception("User not logged in")

        sql = text("DELETE FROM posts WHERE id=:id")
        db.session.execute(sql, {"id": id, "user_id": user_id})
        db.session.commit()
        return True
    except Exception as e:
        print("Error deleting post:", e)
        return False


def search_posts(content, topic_id):
    sql = text("""
        SELECT posts.id, topic_id, posts.content, posts.created_at, topics.title AS topic_title
        FROM posts
        JOIN topics ON posts.topic_id = topics.id
        WHERE posts.content ILIKE :content
        AND topic_id = :topic_id
        ORDER BY posts.created_at DESC
    """)
    result = db.session.execute(sql, {"content": "%" + content + "%", "topic_id": topic_id})
    return result.fetchall()
