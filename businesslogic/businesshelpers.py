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

# This expects queries as an <iterable> of strings
def run_sql_queries(queries):
    conn = mariadb.connect(**db_config)
    
    result = []

    for query in queries:
        cur = conn.cursor(query)
        for (element) in cur:
            result.append(f"{element}")

    cur.execute()

    conn.close()

    return result;
