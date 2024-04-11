import os
class config(object):
    
    OPEN_WEATHER_MAP_APPID = os.environ.get("OPEN_WEATHER_MAP_APPID", None)
    WEATHER_DEFCITY = os.environ.get("WEATHER_DEFCITY", "Anand,India")#city,country

