from sqlalchemy.sql import text
from db import db
from topics import get_topic_count
from posts import get_post_count

def create_region(name, description):
    sql = text("INSERT INTO regions (name, description) VALUES (:name, :description) RETURNING id")
    result = db.session.execute(sql, {"name": name, "description": description})
    db.session.commit()

def get_regions():
    sql = text("SELECT id, name, description FROM regions")
    result = db.session.execute(sql)
    return result.fetchall()


def get_region(id):
    sql = text("SELECT id, name, description FROM regions WHERE id=:id")
    result = db.session.execute(sql, {"id": id})
    return result.fetchone()

def delite_region(name):
    sql = text("DELETE FROM regions WHERE name=:name")
    db.session.execute(sql, {"name": name})
    db.session.commit()

def regions_topics_count():
    sql_regions = text("SELECT * FROM regions")
    regions = db.session.execute(sql_regions)
    regions_l = regions.fetchall()

    regions_topics = {}

    for r in regions_l:
        regions_topics[r[0]] =  get_topic_count(r[0])

    return regions_topics

def regions_posts_count():
    sql_regions = text("SELECT id, name FROM regions")
    regions = db.session.execute(sql_regions).fetchall()

    regions_posts = {}

    for r in regions:
        sql_topics = text("SELECT id FROM topics WHERE region_id=:region_id")
        topics = db.session.execute(sql_topics, {"region_id": r[0]}).fetchall()

        
        post_count = sum(get_post_count(topic[0]) for topic in topics)

        
        regions_posts[r[0]] =  post_count

    return regions_posts
