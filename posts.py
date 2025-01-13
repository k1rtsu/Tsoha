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
