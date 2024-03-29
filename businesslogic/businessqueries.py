def get_available_token_query(userid):
    return ('SELECT users.availabletokenquantity FROM users WHERE users.id='+userid)
