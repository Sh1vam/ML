import os
class config(object):
    
    OPEN_WEATHER_MAP_APPID = os.environ.get("OPEN_WEATHER_MAP_APPID", "4317ba8f763c13b5e4c13118a8c8d9fd")#city,country
    WEATHER_DEFCITY = os.environ.get("WEATHER_DEFCITY", "Anand,India")

