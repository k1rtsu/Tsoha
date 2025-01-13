from flask import session
from sqlalchemy.sql import text
from db import db

def get_comments_count():
    sql = text("SELECT COUNT(*) FROM comments")
    result = db.session.execute(sql)
    return result.fetchone()[0]
