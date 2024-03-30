def get_conditional_user_table_creation_query():
   return 'CREATE TABLE IF NOT EXISTS Users ( username VARCHAR(30), email VARCHAR(30), password VARCHAR(32), availabletokenquantity INT )' 

def get_conditional_reccomandation_table_creation_query():
    return 'CREATE TABLE IF NOT EXISTS Reccomandation ( artistname VARCHAR(32), songname VARCHAR(16), spotifylink VARCHAR(32), FOREIGN KEY (UserID) REFERENCES Users(id) )'

def get_available_token_query(userid):
    return 'SELECT availabletokenquantity FROM Users WHERE Users.id='+userid

def get_reccomandation_for_user_query(userid):
    return 'SELECT artistname, songname, spotifylink FROM Reccomandation WHERE UserID=userid'
