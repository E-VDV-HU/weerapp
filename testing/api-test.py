import requests
import datetime

#config 
unit15oClock = 15

#main garbage
user_city = input("Enter a city: ")
weather_api_location = requests.get(f"https://geocoding-api.open-meteo.com/v1/search?name={user_city}")

print("Starting debugging nonsense, enjoy :)")
print(weather_api_location.json())

longitude = weather_api_location.json()["results"][0]["longitude"]
latitude = weather_api_location.json()["results"][0]["latitude"]
api_city = weather_api_location.json()["results"][0]["name"]

print(f"Config set: \n Longitude: {longitude}, Latitude: {latitude}, City: {api_city}")


weather_data = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=temperature_2m")

print(weather_data.json())

date_now = datetime.datetime.now()
year = datetime.date.today().year
month = datetime.date.today().month
day = datetime.date.today().day
hour = datetime.datetime.now().hour

correct_format = f"{year}-{month:02d}-{day:02d}T{hour:02d}:00"
print(correct_format)

moment_index = weather_data.json()["hourly"]["time"].index(correct_format)
print(moment_index)

# get current temperature
print(weather_data.json()["hourly"]["temperature_2m"][moment_index])

# weather a day in advance (7 days in total)
# api works with own units, adding 24 to unit advances time by 24 hours
# take neutral ground, 15:00 is reasonable.
# 15	"2026-09-07T15:00"

for i in range(7):
    print(f"date: {weather_data.json()['hourly']['time'][unit15oClock]}, temp: {weather_data.json()['hourly']['temperature_2m'][unit15oClock]}")
    unit15oClock += 24

