import urllib
import json
import urllib
import datetime
from google.appengine.api import urlfetch

from models import Destination
from models import get_user


def get_location_new(address):
    """
    Query Google Maps to get GPS coord giving the user destination address. 
    Add Zip code and city to make search better;
    Exctract latitude and longitude, processing the JSON response
    Keyword arguments:
    @param addres: the address whose coords need to be find out
    """
    complete_address = "%s %s" %(address, "70126 Bari")
    data = urllib.urlencode(dict(address=complete_address))
    url ="http://maps.google.com/maps/api/geocode/json?%s=&sensor=false" %data
    result = urlfetch.fetch(url=url,method=urlfetch.GET)
    location = json.loads(result.content)["results"][0]["geometry"]["location"]
    return location["lat"], location["lng"]


def get_stops(latitude, longitude, lines=True):
    """
    Get a next stop, given a latitude and longitude. 
    The stop cannot be the nearest one, because timetable could not be available. 
    
    Keyword arguments:
    @param latitude: the latitude of the user location
    @param longitude: the longitude of user location
    @param lines: a flag, indicating which type of response need to be returned
    """
    url = "http://bari.opendata.planetek.it/OrariBus/v2.1/OpenDataService.svc/REST/rete/FermateVicine/%s/%s/300" %(latitude, longitude)
    result = urlfetch.fetch(url=url,method=urlfetch.GET)
    content = json.loads(result.content)
    stops_id = [resource["IdFermata"] for resource in content]
    i = 0
    url = "http://bari.opendata.planetek.it/OrariBus/v2.1/OpenDataService.svc/REST/OrariPalina/%s/teorico" %stops_id[0]
    result_previsioni = urlfetch.fetch(url=url, method=urlfetch.GET)
    content_previsioni = json.loads(result_previsioni.content)
    i += 1
    while len(content_previsioni["PrevisioniLinee"]) == 0:
        url = "http://bari.opendata.planetek.it/OrariBus/v2.1/OpenDataService.svc/REST/OrariPalina/%s/teorico" %stops_id[i]
        result_previsioni = urlfetch.fetch(url=url, method=urlfetch.GET)
        content_previsioni = json.loads(result_previsioni.content)
        i += 1

    if lines:
        return json.loads(result.content)[i-1]["ListaLinee"]
    return json.loads(result.content)[i-1]


def extract_lines_times(lat, lon, user_id):
    """
    Extract timetables by a stop, retrieving first available stops, using the method above. 
    It matches the user destination informations previously stored in the datastore, 
    with the data retrieved here, in order to propose the smartest solution ever. 

    @param lat: the latitude of user location
    @param lon: the longitude of user location
    @param user_id: the user id, used to retrieve user destination info
    """
    lines_updated_stop = get_stops(lat, lon, lines=False)
    lines_updated = lines_updated_stop["ListaLinee"]
    stop_id = lines_updated_stop["IdFermata"]
    stop_address = lines_updated_stop["DescrizioneFermata"]
    distance_mt = lines_updated_stop["DistanzaMetri"]

    user = get_user(user_id)
    lines_original = json.loads(user.lines)
    intersection = [line for line in lines_updated if line in lines_original]
    url = "http://bari.opendata.planetek.it/OrariBus/v2.1/OpenDataService.svc/REST/OrariPalina/%s/teorico" %stop_id
    result = urlfetch.fetch(url=url, method=urlfetch.GET)

    #estraggo l'elenco degli orari relativi alla fermata che mi interessa
    previsions = json.loads(result.content)["PrevisioniLinee"]
    previsions = filter(lambda prevision: (prevision["Direzione"] ==line["Direzione"] for line in intersection), previsions)
    previsions = filter(lambda prevision: (prevision["IdLinea"] ==line["IdLinea"] for line in intersection), previsions)

    notification_result = [dict(line=prevision["IdLinea"], time=get_time_by_previon(prevision), stop_address=stop_address, distance_mt = distance_mt) for prevision in previsions]
    return notification_result


def get_time_by_previon(prevision):
    """
    Get bus arrival time by an expected result, formatting it for being human readabble
    The function applies some magick trick to retrieve this info, given the odd json response
    Keyword arguments:
    @param prevision: the prevision whose arrrival time needs to be exctracted
    """
    time = int(prevision["OrarioArrivo"].split("(")[1].split(")")[0].split("+")[0])/1000
    time = datetime.datetime.fromtimestamp(time) + datetime.timedelta(hours=1)
    return time.strftime("%H:%M")
