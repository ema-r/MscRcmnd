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

def run_sql_query(my_query):
    conn = mariadb.connect(**db_config)
    
    cur = conn.cursor()

    result = []

    rows = cur.execute(my_query)
    if rows is not None:
        for (element) in cur:
            result.append(f"{element}")

    conn.close()

    return result;


# This expects queries as an <iterable> of strings
def run_sql_queries(queries):

    result = []

    for qry in queries:
        result.append(run_sql_query(qry))

    return result;
