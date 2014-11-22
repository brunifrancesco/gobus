import webapp2
import json
from service import get_location_new
from service import get_stops
from service import extract_lines_times

from dao import store_user_destination


class HomeHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write("<h1>GoBus server app</h1>")


class MainHandler(webapp2.RequestHandler):

    def post(self):
        self.response.headers['Content-Type'] = "application/json"
        destination = self.request.get('destination')
        user_id = self.request.get('user_id')
	response = get_location_new(destination)
        lines = get_stops(response[0], response[1])
        store_user_destination(user_id=user_id, destination=destination, lines=lines)
        self.response.write(json.dumps(dict(response="Ok")))


class StopsHandler(webapp2.RequestHandler):
    def post(self):
        self.response.headers['Content-Type'] = "application/json"
        lat = self.request.get('latitude')
        lon = self.request.get('longitude')
        user_id = self.request.get('user_id')
        notification_result = extract_lines_times(lat, lon, user_id)
        self.response.write(json.dumps(dict(result=notification_result)))

app = webapp2.WSGIApplication([
    ('/', HomeHandler),
    ('/init', MainHandler),
    ('/stops', StopsHandler),
], debug=False)
