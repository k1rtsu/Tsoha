import os
from flask import Flask
from db import db

app = Flask(__name__)

@app.cli.command("init-db")
def init_db():
    """Luo tietokantataulut"""
    with app.app_context():
        with open("schema.sql", "r") as f:
            db.session.execute(f.read())
            db.session.commit()
        print("Tietokantataulut luotu!")
