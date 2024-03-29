from flask import Flask, jsonify
import json
import mariadb
import sys

# Defined by us
import businessqueries as bqueries
import businesshelpers as bhelpers

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

# Route to receive info on available number of tokens to request services
@server.route('/availabletokens/<userid>')
def availabletokens(userid):
    conn = mariadb.connect(**db_config)

    availabletokens = []    # Should be a single element, but just to be sure...
    # Maybe add exception too if number of elements is anomalous?

    cur = conn.cursor()
    cur.execute(bqueries.get_available_token_query(userid));

    for (availabletokennumber) in cur:
        availabletokens.append(f"{availabletokennumber}");

    conn.close()
    
    return jsonify(availabletokens)
    


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




