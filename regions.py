from flask import session
from sqlalchemy.sql import text
from db import db

def create_region(name, description):
    sql = text("INSERT INTO regions (name, description) VALUES (:name, :description) RETURNING id")
    result = db.session.execute(sql, {"name": name, "description": description})
    db.session.commit()

def get_regions():
    sql = text("SELECT id, name, description FROM regions")
    result = db.session.execute(sql)
    return result.fetchall()

def delite_region(id):
    sql = text("DELETE FROM regions WHERE id=:id")
    db.session.execute(sql, {"id": id})
    db.session.commit()

def get_region(id):
    sql = text("SELECT id, name, description FROM regions WHERE id=:id")
    result = db.session.execute(sql, {"id": id})
    return result.fetchone()

def delite_region(name):
    sql = text("DELETE FROM regions WHERE name=:name")
    db.session.execute(sql, {"name": name})
    db.session.commit()
    