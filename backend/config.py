import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://postgres:pass@localhost:5432/coffeeshop')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
