import os
from flask import Flask
import mysql.connector


class DBManager:
    def __init__(self, database='test', host="db", user="root", password_file=None):
        pf = open(password_file, 'r')
        self.connection = mysql.connector.connect(
            user=user, 
            password='test',
            host=host,
            database=database,
            auth_plugin='mysql_native_password'
        )
        pf.close()
        self.cursor = self.connection.cursor()
    
    def populate_db(self):
        self.cursor.execute('DROP TABLE IF EXISTS example')
        self.cursor.execute('CREATE TABLE example)')
        self.connection.commit()


server = Flask(__name__)
conn = None

@server.route('/')
def hello():
    global conn
    if not conn:
        conn = DBManager(password_file='/run/secrets/db-password')
        conn.populate_db()
    return "db setup\n"


if __name__ == '__main__':
    server.run()
