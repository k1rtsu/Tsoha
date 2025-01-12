from flask import session
from sqlalchemy.sql import text
from db import db

def create_post(topic_id, content):
    sql = text("INSERT INTO posts (topic_id, content) VALUES (:topic_id, :content) RETURNING id")
    result = db.session.execute(sql, {"topic_id": topic_id, "content": content})


def get_post(name):
    sql = text("SELECT id, topic_id, content FROM posts WHERE name=:name")
    result = db.session.execute(sql, {"name": name})
    return result.fetchone()

def get_posts():
    sql = text("SELECT id, topic_id, content FROM posts")
    result = db.session.execute(sql)
    return result.fetchall()

def get_post_count(topic_id):
    sql = text("SELECT COUNT(*) FROM posts WHERE topic_id=:topic_id")
    result = db.session.execute(sql, {"topic_id": topic_id})
    return result.fetchone()[0]
