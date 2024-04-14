def get_conditional_user_table_creation_query():
   return 'CREATE TABLE IF NOT EXISTS Users ( uid int(11) NOT NULL AUTO_INCREMENT, username varchar(30) NOT NULL, email varchar(30) NOT NULL, password varchar(32) NOT NULL, PRIMARY KEY (uid), UNIQUE( username ), UNIQUE( email ) );' 

def get_conditional_reccomandation_table_creation_query():
    return 'CREATE TABLE IF NOT EXISTS Reccomandation ( rid int(11) NOT NULL, artistname varchar(32) NOT NULL, songname varchar(16) NOT NULL, spotifylink varchar(32) NOT NULL, userID int(11), PRIMARY KEY(rid) , FOREIGN KEY (userID) REFERENCES Users(uid) );'

def get_available_token_query(userid):
    return 'SELECT availabletokenquantity FROM Users WHERE Users.uid='+userid+';'

def get_reccomandation_for_user_query(userid):
    return 'SELECT artistname, songname, spotifylink FROM Reccomandation WHERE UserID='+userid+';'

def insert_user_query(username, email, password):
    return f"INSERT INTO Users (username, email, password) VALUES ('{username}', '{email}', '{password}');"

def get_user_data_query(userid):
    return 'SELECT username, email FROM Users WHERE Users.uid='+userid+';'

# These three now return the value itself just for testing. We need to replace them with COUNT(1)
def get_user_by_id(userid):
    return 'SELECT username FROM Users WHERE Users.uid='+userid+';'

def get_user_by_username(username):
    return f"SELECT username FROM Users WHERE Users.username='{username}';"

def get_user_by_email(email):
    return 'SELECT email FROM Users WHERE Users.email='+email+';'

# Mostly a debug funcion
def show_all_users():
    return "SELECT * FROM Users;"
