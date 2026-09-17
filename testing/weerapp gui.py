import tkinter as tk
import requests
import datetime

# placeholders for devving
user_city = "Utrecht"
latitude = 31.2
longitude = 31.2
index_modifier = 0
index_hours = 24
moment_index = 0

#config
weather_api_location = f"https://geocoding-api.open-meteo.com/v1/search?name={user_city}"
weather_data = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=temperature_2m"
unit15oClock = 15

#functions
def convert_user_location(city_entry):
    request_dipshit = requests.get(f"https://geocoding-api.open-meteo.com/v1/search?name={city_entry}")
    longitude = request_dipshit.json()["results"][0]["longitude"] # needed for api call
    latitude = request_dipshit.json()["results"][0]["latitude"] # needed for api call
    api_city = request_dipshit.json()["results"][0]["name"] # needed for gui correct spelling
    api_country = request_dipshit.json()["results"][0]["country_code"] # needed for gui (finishing touches)
    return longitude, latitude, api_city, api_country

def actual_weahter_data(longitude, latitude): # converting place to cords for api to use
    request_forcast = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=temperature_2m")
    return request_forcast.json()

def convert_time_to_unit(weather_data): # converting readable time to fk shit unit of api
    year = datetime.date.today().year
    month = datetime.date.today().month
    day = datetime.date.today().day
    hour = datetime.datetime.now().hour
    correct_format = f"{year}-{month:02d}-{day:02d}T{hour:02d}:00"
    moment_index = weather_data.json()["hourly"]["time"].index(correct_format)
    return moment_index, correct_format

def get_current_temp(weather_data, moment_index,index_modifier,index_hours): # get current temperature at this moment
    return weather_data.json()["hourly"]["temperature_2m"][moment_index + index_modifier*index_hours]

def get_next_days_temp(weather_data, unit15oClock): # 7 day forcast
    temperatures = []
    for i in range(7):
        temperature = weather_data.json()["hourly"]["temperature_2m"][unit15oClock]
        temperatures.append(temperature)
        unit15oClock += 24
    return temperatures

def get_gui_data(city_entry,longitude, latitude, weather_data, moment_index,index_modifier,index_hours,unit15oClock):
    convert_user_location(city_entry)
    actual_weahter_data(longitude, latitude)
    convert_time_to_unit(weather_data)
    get_current_temp(weather_data, moment_index,index_modifier,index_hours)
    get_next_days_temp(weather_data, unit15oClock)
    return convert_user_location(city_entry), actual_weahter_data(longitude, latitude), convert_time_to_unit(weather_data), get_current_temp(weather_data, moment_index,index_modifier,index_hours), get_next_days_temp(weather_data, unit15oClock)


# gui

root = tk.Tk()
root.title("Esper's Weather App")
root.geometry("900x600") #size

# top frame for city entry and refresh button
top_frame = tk.Frame(root)
top_frame.pack(side="top", pady=20)

city_entry = tk.Entry(top_frame)
city_entry.pack(side="left", padx=5)

# side for 7 day forcast
side_forcast_frame = tk.Frame(root)
side_forcast_frame.pack(side="right", padx=20)

button = tk.Button(top_frame, text="refresh", command=lambda: get_gui_data(city_entry, longitude, latitude, weather_data, moment_index, index_modifier, index_hours, unit15oClock), padx=5)
button.pack(side="left")

root.mainloop()