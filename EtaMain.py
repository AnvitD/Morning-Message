import datetime
import googlemaps
import time

from sys import path
path.append('Insert pathway to the folder with the requests module here')
import requests
import os
import string

weather_key_api = 'Insert api key here'

town = "Insert your town here"

#URL is constructed using f string
url = f'http://api.openweathermap.org/data/2.5/weather?q={town}&appid={weather_key_api}'

#the requests module is used to send an HTTP GET request to the URL and the response is stored in the response variable
response = requests.get(url)
#this function converts the temperature from Kelvin to Fahrenheit
def ktof(temp):
    global tempf
    tempf = (float(temp)-273.15)*1.8+32
    return tempf
    
#the status code for a successful request is 200
#if the status code is 200, the code will gather the data from the OpenWeatherMap API and print it onto the screen
if response.status_code == 200:
    data = response.json() #the JSON method converts the HTML data into a python dictionary
    temp = data['main']['temp']
    desc = data['weather'][0]['description']
    caps = string.capwords(desc)
    
else:
    print('Weather data for this city does not exist.') #if the request was unsuccessful, this message will print
    
if response.status_code == 200:
    print("")
else:
    print("") 


#This function calls on google maps to get an Estimated travel time to your destination.
def get_eta():
    starting_location = "Enter Starting location here"
    end_location = "Enter Destination Location here"

    map_api_key = "Insert key here"
    gmaps = googlemaps.Client(key=map_api_key)

    directions = gmaps.directions(starting_location, end_location)
    first_leg = directions[0]['legs'][0]
    duration = first_leg['duration']["text"]
    return duration
 
#This function allows python to access Twilio account and send text messages. 
def send_message(message): 
    twilio_account_sid = "Twilio_account_sid"
    twilio_account_token = "twilio_account_token"
    twilio_phone_num = "twilio_phone_num"
    receiving_phone_num = "sender_phone_num"
    Client = Client(twilio_account_sid, twilio_account_token)

    Client.message.client(
        to=receiving_phone_num,
        from_=twilio_phone_num, 
        body=message 
    )

def main():
    duration = get_eta()

    time = datetime.time(hour=8, minute=00) #Sets the desired time to pull data from google maps
    arivaltime = ( time + duration).strftime('%I:%M %p') #Calculates the arrival time at the destination. 

    message = (
        f"Good Morning!!/n/n"
        f"Today's weather is: {str(int(ktof(temp)))}/n"
        f"Sky Conditions: {str(caps)}/n/n"
        f"Today's Estimate time from Home to College: {duration}./n"
        f"Leave Parking Garage by:{time} to arrive at destination by {arivaltime}"
    )

    send_message(message) 

while True: 
    if datetime.time(hour=8, minute=00):
        if __name__ == "__main__":
            main() 
