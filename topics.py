from flask import session
from sqlalchemy.sql import text
from db import db

def get_topics(region_id):
    sql = text("SELECT id, region_id, title, description FROM topics WHERE region_id=:region_id")
    result = db.session.execute(sql, {"region_id": region_id})
    return result.fetchall()

def get_topic(id):
    sql = text("SELECT id, region_id, title, description FROM topics WHERE id=:id")
    result = db.session.execute(sql, {"id": id})
    return result.fetchone()

def get_topic_count(region_id):
    sql = text("SELECT COUNT(*) FROM topics WHERE region_id=:region_id")
    result = db.session.execute(sql, {"region_id": region_id})
    return result.fetchone()[0]

def topic_posts_count(topic_id):
    sql = text("SELECT COUNT(*) FROM posts WHERE topic_id=:topic_id")
    result = db.session.execute(sql, {"topic_id": topic_id})
    return result.fetchone()[0]

def create_topic(region_id, title, description, user_id):
    try:
        sql = text("""
            INSERT INTO topics (region_id, title, description, created_by)
            VALUES (:region_id, :title, :description, :user_id)
        """)
        db.session.execute(sql, {"region_id": region_id, "title": title, "description": description, "user_id": user_id})
        db.session.commit()
        return True
    except Exception as e:
        print("Error creating topic:", e)
        return False
    
def delete_topic(topic_id):
    sql = text("""
        DELETE FROM topics
        WHERE id = :topic_id
    """)
    db.session.execute(sql, {"topic_id": topic_id})
    db.session.commit()

def get_author(topic_id):
    sql = text("SELECT created_by FROM topics WHERE id=:topic_id")
    result = db.session.execute(sql, {"topic_id": topic_id})
    return result.fetchone()[0]