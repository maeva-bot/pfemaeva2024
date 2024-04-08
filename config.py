import os

class Config:
    SECRET_KEY = 'thisisasecretkey'
    SQLALCHEMY_DATABASE_URI =  'mysql+pymysql://root:@localhost:3306/pfe2024_2'
    SQLALCHEMY_TRACK_MODIFICATIONS = False