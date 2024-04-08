def get_conditional_user_table_creation_query():
   return 'CREATE TABLE IF NOT EXISTS Users ( uid int(11) NOT NULL AUTO_INCREMENT, username varchar(30) NOT NULL, email varchar(30) NOT NULL, password varchar(32) NOT NULL, availabletokenquantity int NOT NULL, PRIMARY KEY (uid) );' 

def get_conditional_reccomandation_table_creation_query():
    return 'CREATE TABLE IF NOT EXISTS Reccomandation ( rid int(11) NOT NULL, artistname varchar(32) NOT NULL, songname varchar(16) NOT NULL, spotifylink varchar(32) NOT NULL, userID int(11), PRIMARY KEY(rid) , FOREIGN KEY (userID) REFERENCES Users(uid) );'

def get_available_token_query(userid):
    return 'SELECT availabletokenquantity FROM Users WHERE Users.id='+userid+';'

def get_reccomandation_for_user_query(userid):
    return 'SELECT artistname, songname, spotifylink FROM Reccomandation WHERE UserID=userid;'

def insert_user_query(username, email, password):
    return "INSERT INTO Users (username, email, password) VALUES ('{username}', '{email}', '{password}');"
