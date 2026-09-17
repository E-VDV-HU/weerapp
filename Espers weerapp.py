import tkinter as tk
import requests
import datetime
from tkinter import messagebox
from tkinter import PhotoImage
from PIL import Image, ImageTk
import os 

# placeholders for devving
user_city = "Utrecht"
latitude = 31.2
longitude = 31.2
index_modifier = 0
index_hours = 24
moment_index = 0

#config
unit15oClock = 15
geometry = "1200x800"
title_tk = "Esper's Weather App"

#autoconfig
dir_path = os.path.dirname(os.path.realpath(__file__))
geometry_y = geometry.split("x")[1]
geometry_x = geometry.split("x")[0]

#image config
error = f"{dir_path}/assets/generic/error.png"
notice = f"{dir_path}/assets/generic/notice.png"
clear_sky = f"{dir_path}/assets/gui icons weahtercode/clear_sky.png"
Depositing_rime_fog = f"{dir_path}/assets/gui icons weahtercode/Depositing_rime_fog.png"
Drizzle_Dense_intensity = f"{dir_path}/assets/gui icons weahtercode/Drizzle_Dense_intensity.png"
Drizzle_Light_intensity = f"{dir_path}/assets/gui icons weahtercode/Drizzle_Light_intensity.png"
Drizzle_Moderate_intensity = f"{dir_path}/assets/gui icons weahtercode/Drizzle_Moderate_intensity.png"
Fog = f"{dir_path}/assets/gui icons weahtercode/Fog.png"
Freezing_Drizzle_Dense_intensity = f"{dir_path}/assets/gui icons weahtercode/Freezing_Drizzle_Dense_intensity.png"
Freezing_Drizzle_Light_intensity = f"{dir_path}/assets/gui icons weahtercode/Freezing_Drizzle_Light_intensity.png"
Mainly_clear = f"{dir_path}/assets/gui icons weahtercode/Mainly_clear.png"
Overcast = f"{dir_path}/assets/gui icons weahtercode/Overcast.png"
Partly_cloudy = f"{dir_path}/assets/gui icons weahtercode/Partly_cloudy.png"
Rain_Heavy_intensity = f"{dir_path}/assets/gui icons weahtercode/Rain_Heavy_intensity.png"
Rain_Moderate_intensity = f"{dir_path}/assets/gui icons weahtercode/Rain_Moderate_intensity.png"
Rain_Slight_intensity = f"{dir_path}/assets/gui icons weahtercode/Rain_Slight_intensity.png"

#functions
def convert_user_location(city_entry):
    try:
        request_dipshit = requests.get(f"https://geocoding-api.open-meteo.com/v1/search?name={city_entry}")
        request_dipshit.raise_for_status() # raise an error if the request failed
        longitude = request_dipshit.json()["results"][0]["longitude"] # needed for api call
        latitude = request_dipshit.json()["results"][0]["latitude"] # needed for api call
        api_city = request_dipshit.json()["results"][0]["name"] # needed for gui correct spelling
        api_country = request_dipshit.json()["results"][0]["country_code"] # needed for gui (finishing touches)
        return longitude, latitude, api_city, api_country
    except (KeyError, IndexError):
        messagebox.showerror("Error", f"a City named {city_entry} could not found")
        return None, None, None, None

def retrieve_weahter_data(longitude, latitude): # converting place to cords for api to use
    request_forcast = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=temperature_2m,weather_code,rain,precipitation_probability&timezone=auto")
    return request_forcast.json()

def convert_time_to_unit(weather_data): # converting readable time to the fk shit unit of api
    year = datetime.date.today().year
    month = datetime.date.today().month
    day = datetime.date.today().day
    hour = datetime.datetime.now().hour
    correct_format = f"{year}-{month:02d}-{day:02d}T{hour:02d}:00"
    moment_index = weather_data["hourly"]["time"].index(correct_format)
    return moment_index, correct_format

def get_current_temp(weather_data, moment_index,index_modifier,index_hours): # get current temperature at this moment
    return weather_data["hourly"]["temperature_2m"][moment_index + index_modifier*index_hours]

def get_current_weathercode(weather_data, moment_index,index_modifier,index_hours): # get current weather code at this moment
    return weather_data["hourly"]["weather_code"][moment_index + index_modifier*index_hours]

def get_current_rain(weather_data, moment_index,index_modifier,index_hours): # get current rain at this moment
    rain = weather_data["hourly"]["rain"][moment_index + index_modifier*index_hours]
    return rain

def initialize_gui_icon(weather_data_json, moment_index):
    global photo_weathercode
    code = weather_data_json["hourly"]["weather_code"][moment_index]
    if code == 0:
        image_weathercode = Image.open(clear_sky)
    elif code == 1:
        image_weathercode = Image.open(Mainly_clear)
    elif code == 2:
        image_weathercode = Image.open(Partly_cloudy)
    elif code == 3:
        image_weathercode = Image.open(Overcast)
    elif code == 45:
        image_weathercode = Image.open(Fog)
    elif code == 48:
        image_weathercode = Image.open(Depositing_rime_fog)
    elif code == 51:
        image_weathercode = Image.open(Drizzle_Light_intensity)
    elif code == 53:
        image_weathercode = Image.open(Drizzle_Moderate_intensity)
    elif code == 55:
        image_weathercode = Image.open(Drizzle_Dense_intensity)
    elif code == 56:
        image_weathercode = Image.open(Freezing_Drizzle_Light_intensity)
    elif code == 57:
        image_weathercode = Image.open(Freezing_Drizzle_Dense_intensity)
    elif code == 61:
        image_weathercode = Image.open(Rain_Slight_intensity)
    elif code == 63:
        image_weathercode = Image.open(Rain_Moderate_intensity)
    elif code == 65:
        image_weathercode = Image.open(Rain_Heavy_intensity)
    else:
        image_weathercode = Image.open(notice)

    image_weathercode = image_weathercode.resize((50, 50))
    photo_weathercode = ImageTk.PhotoImage(image_weathercode)
    weather_code_image.config(image=photo_weathercode)

def get_next_days_temp(weather_data, unit15oClock): # 7 day forcast
    temperatures = []
    for i in range(7):
        temperature = weather_data["hourly"]["temperature_2m"][unit15oClock]
        temperatures.append(temperature)
        unit15oClock += 24
    return temperatures

def refresh(): #main function for button to call, gets all the data and returns it to the gui
    city = city_entry.get()
    longitude, latitude, api_city, api_country = convert_user_location(city)
    weather_data_json = retrieve_weahter_data(longitude, latitude)
    moment_index, correct_format = convert_time_to_unit(weather_data_json)
    current_temp = get_current_temp(weather_data_json, moment_index, index_modifier, index_hours)
    next_days_temp = get_next_days_temp(weather_data_json, unit15oClock)
    current_weathercode = get_current_weathercode(weather_data_json, moment_index, index_modifier, index_hours)
    current_rain = get_current_rain(weather_data_json, moment_index, index_modifier, index_hours)
    initialize_gui_icon(weather_data_json,moment_index)
    #convert to gui data
    current_temp_gui.set(f"{current_temp} °C")
    current_city_gui.set(f"{api_city}, {api_country}")
    current_weathercode_gui.set(f"{current_weathercode}")
    current_rain_gui.set(f"{current_rain} mm")

    # 7 day forcast
    for i, temperature in enumerate(next_days_temp):
        day_gui[i].set(f"{temperature} °C")

    # 12 hour forcast
    day_index=moment_index
    for j in range(12):
        time = weather_data_json["hourly"]["time"][day_index].split("T")[1]
        temperature = weather_data_json["hourly"]["temperature_2m"][day_index]
        rain = weather_data_json["hourly"]["rain"][day_index]
        precipitation_probability = weather_data_json["hourly"]["precipitation_probability"][day_index]

        hour_gui[j].set(f"{time}: \n {temperature} °C \n {rain} mm \n {precipitation_probability}%")
        day_index += 1


#tkinter gui
root = tk.Tk()
#gui config
root.title(title_tk) #title
root.geometry(geometry) #size

# gui placeholders
current_temp_gui = tk.StringVar()
current_city_gui = tk.StringVar()
current_weathercode_gui = tk.StringVar()
current_rain_gui = tk.StringVar()
image_weathercode = Image.open(notice) # image call
image_weathercode = image_weathercode.resize((50, 50))
photo_weathercode = ImageTk.PhotoImage(image_weathercode) #image initialize

day_gui = [tk.StringVar() for _ in range(7)]
hour_gui = [tk.StringVar() for _ in range(12)]


# gui building
# frame w/ location txt box and refresh button
top_frame = tk.Frame(root)
top_frame.pack(side="top", pady=20)
button = tk.Button(top_frame, text="refresh", command=refresh)
button.pack(side="right", padx=5)
city_entry = tk.Entry(top_frame)
city_entry.insert(0, user_city)
city_entry.pack(side="left", padx=5)


# side frame for 7 day forcast
side_forcast_frame = tk.Frame(root, bg="grey", width=200, height=600)
side_forcast_frame.pack(side="right", padx=20)
tk.Label(side_forcast_frame, text="7 Day Forecast", font=("Helvetica", 18)).pack(pady=10)
for day in day_gui:
    tk.Label(side_forcast_frame, textvariable=day, font=("Helvetica", 14)).pack(pady=5)

# temperature in the middle
middle_frame = tk.Frame(root, bg="grey", width=geometry_x, height=geometry_y)
middle_frame.place(relx=0.5, rely=0.5, anchor="center")
combi_icon_cityname = tk.Frame(middle_frame, bg="grey")
combi_icon_cityname.pack(pady=10)
current_city_label = tk.Label(combi_icon_cityname, textvariable=current_city_gui, font=("Helvetica", 24))
current_city_label.pack(pady=10, side="left")
weather_code_image = tk.Label(combi_icon_cityname, image=photo_weathercode)
weather_code_image.pack(pady=10, side="right", padx=10)
current_temp_label = tk.Label(middle_frame, textvariable=current_temp_gui, font=("Helvetica", 48))
current_temp_label.pack(pady=20)
hourly_frame = tk.Frame(middle_frame, bg="grey", width=300, height=100)
hourly_frame.pack(pady=20)
for hour in hour_gui:
    tk.Label(hourly_frame, textvariable=hour, font=("Helvetica", 12)).pack(side="left", pady=2)

refresh() # initial refresh to populate the gui with data
root.mainloop()
