from google.appengine.ext import db


class Destination(db.Model):
    """Models an individual destination entity"""
    author = db.IntegerProperty()
    destination = db.StringProperty(indexed=False)
    lines = db.StringProperty(indexed=False)


def get_user(user_id):
    """
    Helper method to retrieve user info, by user_id
    """
    users = db.GqlQuery("SELECT * FROM Destination WHERE author = 0")
    for user in users:
        return user
