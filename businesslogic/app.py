from flask import Flask, jsonify
import json
import mariadb
import sys

# Defined by us
import businessqueries as bqueries
import businesshelpers as bhelpers

server = Flask(__name__)
server.config["DEBUG"] = True

@server.route('/')
def hello():
    # conn = mariadb.connect(**db_config)
    conn = mariadb.connect(**bhelpers.get_db_config())
            
    cur = conn.cursor()
    cur.execute('DROP TABLE IF EXISTS users')
    cur.execute(bqueries.get_table_creation_query())
    conn.close()

    return "db setup success\n"

# Route to receive info on available number of tokens to request services
@server.route('/availabletokens/<userid>')
def availabletokens(userid):
    # conn = mariadb.connect(**db_config)
    conn = mariadb.connect(**bhelpers.get_db_config())

    availabletokens = []    # Should be a single element, but just to be sure...
    # Maybe add exception too if number of elements is anomalous?

    cur = conn.cursor()
    cur.execute(bqueries.get_available_token_query(userid));

    for (availabletokennumber) in cur:
        availabletokens.append(f"{availabletokennumber}");

    conn.close()
    
    return jsonify({'available_tokens': availabletokens})


@server.route('/prevracc')
# Instantiate Connection
def racc():
    try:
     conn = mariadb.connect(**bhelpers.get_db_config())
     # Instantiate Cursor
     cur = conn.cursor()
     conn.close()
     return "db prevracc suc"
     # Close Connection
    
    except mariadb.Error as e:
      print(f"Error connecting to the database: {e}")
      sys.exit(1)


if __name__ == '__main__':
    server.run()




