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
    cur.execute('CREATE TABLE example ( a INT )')
    conn.close()
    return "db setup success\n"



@server.route('/prevracc')
# Instantiate Connection
def racc():
    try:
     conn = mariadb.connect(
        **db_config
        
    )
     # Instantiate Cursor
     cur = conn.cursor()

     return "db prevracc suc"
     # Close Connection
     conn.close()
    
    except mariadb.Error as e:
      print(f"Error connecting to the database: {e}")
      sys.exit(1)



if __name__ == '__main__':
    server.run()

