from flask import Flask
import json
import mariadb

server = Flask(__name__)
server.config["DEBUG"] = True

db_config = {
        'host': 'db',
        'port': 3306,
        'user': 'test_user',
        'password': 'test',
        'database': 'test_database'
        }

@server.route('/')
def hello():
    conn = mariadb.connect(**db_config)
            
    cur = conn.cursor()
    cur.execute('DROP TABLE IF EXISTS example')
    cur.execute('CREATE TABLE example)')

    return "db setup\n"


if __name__ == '__main__':
    server.run()

