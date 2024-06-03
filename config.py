# config.py

import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "VEVTVFNFQ1JFVEtFWQ=="
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("DATABASE_URL") or "mysql://admin:admin@localhost/testdb"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
