from models import Destination
import json


def store_user_destination(user_id, destination, lines):
    """
    Store user info, for further retrieving.
    
    Keyword arguments:
    @param user_id: the unique user key, used to retrieve user details
    @param destination: the destination, provided in the first user interaction
    @param lines: a json string to represent useful bus lines to reach the destination
    """
    destination = Destination(author=user_id, destination=destination, lines=json.dumps(lines))
    destination.put()
