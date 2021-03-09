from flaskr.db import get_db

class UserModel():
    
    def __init__(self, username, password, type):
        self._username = username
        self._password = password
        self._type = type#interno, portal
    
    def check_password(self, password):
        return password == self._password