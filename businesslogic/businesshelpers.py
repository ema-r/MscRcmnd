from flask import jsonify
import mariadb

db_config = {
        'host': 'db',
        'port': 3306,
        'user': 'test_user',
        'password': 'test',
        'database': 'test_database'
        }

def get_db_config():
    return db_config

def json_return(mystring):
    return jsonify({'returned': mystring})


# flag = True -> SELECT QUERY
# flag = False -> INSERT QUERY
# Default -> False
def run_sql_query(my_query, flag=False):
    print(my_query)

    try:
        conn = mariadb.connect(**db_config)
    except mariadb.Error as e:
        print (f"Error connecting to MariaDB Platform: {e}")
        return f"Error connecting to MariaDB: {e}"
    
    # Get the DB cursor 
    cur = conn.cursor()

    try:
        cur.execute(my_query)
    except mariadb.Error as e:
        print(f"Error: {e}")
        return f"Error: {e}"

    result = True

    # SELECT QUERY
    # TO-BE completed (useful to allow login)
    if flag==True:
        result=cur.fetchall()

    else: conn.commit()

    conn.close()

    return result


# This expects queries as an <iterable> of strings
def run_sql_queries(queries):

    result = []

    for qry in queries:
        result.append(run_sql_query(qry))

    return result
