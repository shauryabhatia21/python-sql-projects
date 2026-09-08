import os
import mysql.connector as m1

def get_connection():
    # Enter your MySQL credentials here or set environment variables:
    db_host = os.getenv('DB_HOST', 'localhost')
    db_user = os.getenv('DB_USER', 'root')
    db_password = os.getenv('DB_PASSWORD', 'YOUR_PASSWORD')
    db_name = os.getenv('DB_NAME', 'ots')
    return m1.connect(host=db_host, database=db_name, user=db_user, password=db_password)
