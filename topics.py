from flask import session
from sqlalchemy.sql import text
from db import db


def create_topic(name, description):
    sql = text("INSERT INTO topics (name, description) VALUES (:name, :description) RETURNING id")
    result = db.session.execute(sql, {"name": name, "description": description})
    db.session.commit()

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
