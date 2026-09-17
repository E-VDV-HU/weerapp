# Esper's Weather App
(readme made by copilot on github, rest is my code)
A simple desktop weather application built with Python and Tkinter. It fetches live weather data from the Open-Meteo API and displays the current conditions, a 12-hour outlook, and a 7-day forecast for a chosen city.

## Features

- Search for weather by city name
- Show the current temperature in °C
- Display current rain amount and precipitation probability
- View a 12-hour forecast with time, temperature, and rainfall
- View a 7-day forecast
- Show weather condition icons using local asset images
- Clean desktop UI built with Tkinter

## Screenshots

The app includes a desktop dashboard with:

- a city search field and refresh button
- the current city label and temperature
- a weather icon matching the current conditions
- a compact hourly summary
- a 7-day forecast sidebar

## Technologies Used

- Python 3
- Tkinter for the GUI
- Requests for API calls
- Pillow for image handling
- Open-Meteo geocoding and forecast APIs

## Project Structure

- `Espers weerapp.py` — main application entry point
- `assets/` — weather icon assets used by the GUI
- `testing/` — small experimental scripts and test files
- `README.md` — project documentation

## Requirements

Before running the app, install the necessary Python packages:

```bash
pip install requests pillow
```

If you are using a Linux distribution, you may also need the Tkinter runtime packages installed for your system.

## Running the App

From the repository root, run:

```bash
python "Espers weerapp.py"
```

On some systems, you may need to use:

```bash
python3 "Espers weerapp.py"
```

## How to Use

1. Open the app.
2. Enter a city name in the text field.
3. Click the Refresh button.
4. The app will fetch the weather for that city and update the dashboard.

If the city cannot be found, an error message will appear.

## Data Source

This project uses the Open-Meteo API:

- Geocoding: `https://geocoding-api.open-meteo.com/v1/search`
- Forecast: `https://api.open-meteo.com/v1/forecast`

## Notes

- This is a lightweight personal weather dashboard, intended for learning and experimentation.
- Weather data depends on the Open-Meteo API and internet connectivity.
- The project does not currently include an explicit license file.

## Future Improvements

Possible enhancements include:

- dark mode / theme support
- unit switching (Celsius/Fahrenheit)
- more detailed weather metrics
- better error handling and validation
- packaging into an executable for Windows/macOS/Linux
