def get_table_creation_query():
   return 'CREATE TABLE users ( username VARCHAR(30), email VARCHAR(30), password VARCHAR(32), availabletokenquantity INT )' 

def get_available_token_query(userid):
    return 'SELECT users.availabletokenquantity FROM users WHERE users.id='+userid
