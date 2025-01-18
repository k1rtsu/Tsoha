from flask import session
from sqlalchemy.sql import text
from db import db

def create_comment(post_id, content):
    try:
        user_id = session.get("user_id")
        if not user_id:
            raise Exception("User not logged in")

        sql = text("""
            INSERT INTO comments (post_id, user_id, content)
            VALUES (:post_id, :user_id, :content)
        """)

        db.session.execute(sql, {"post_id": post_id, "user_id": user_id, "content": content})
        db.session.commit()
        return True
    except Exception as e:
        print("Error creating comment:", e)
        return False


def get_comments_for_post(post_id):
    sql = text("""
        SELECT 
            comments.id AS comment_id,
            comments.content AS comment_content,
            comments.created_at AS comment_created_at,
            users.username AS author_name
        FROM comments
        LEFT JOIN users ON comments.user_id = users.id
        WHERE comments.post_id = :post_id
        ORDER BY comments.created_at ASC
    """)
    result = db.session.execute(sql, {"post_id": post_id})
    return result.fetchall()
