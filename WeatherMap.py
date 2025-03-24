import folium
from folium.elements import Element
import requests
import json
from Key import api_key

# cities i would like to display
cities = {
    "Boise": (43.615, -116.202),
    "Meridian": (43.6121, -116.3915),
    "Nampa": (43.5607, -116.5635),
    "Idaho Falls": (43.4917, -112.0337),
    "Pocatello": (42.8713, -112.4455),
    "Caldwell": (43.6629, -116.6874),
    "Coeur d'Alene": (47.6777, -116.7805),
    "Twin Falls": (42.5628, -114.4609),
    "Rexburg": (43.826, -111.789),
    
    # State Capitals
    "Montgomery": (32.3777, -86.3006),
    "Juneau": (58.3019, -134.4197),
    "Phoenix": (33.4484, -112.074),
    "Little Rock": (34.7465, -92.2896),
    "Sacramento": (38.5816, -121.4944),
    "Denver": (39.7392, -104.9903),
    "Hartford": (41.7658, -72.6734),
    "Dover": (39.1582, -75.5244),
    "Tallahassee": (30.4383, -84.2807),
    "Atlanta": (33.749, -84.388),
    "Honolulu": (21.3069, -157.8583),
    "Des Moines": (41.5868, -93.625),
    "Springfield": (39.798, -89.6444),
    "Indianapolis": (39.7684, -86.1581),
    "Topeka": (39.0473, -95.6752),
    "Frankfort": (38.2009, -84.8733),
    "Baton Rouge": (30.4515, -91.1871),
    "Augusta": (44.3106, -69.7795),
    "Annapolis": (38.9784, -76.4922),
    "Boston": (42.3601, -71.0589),
    "Lansing": (42.7325, -84.5555),
    "St. Paul": (44.9537, -93.09),
    "Jackson": (32.2988, -90.1848),
    "Jefferson City": (38.5767, -92.1735),
    "Helena": (46.5884, -112.024),
    "Lincoln": (40.8136, -96.7026),
    "Carson City": (39.1638, -119.7674),
    "Concord": (43.2081, -71.5376),
    "Trenton": (40.2171, -74.7429),
    "Santa Fe": (35.687, -105.9378),
    "Albany": (42.6526, -73.7562),
    "Raleigh": (35.7796, -78.6382),
    "Bismarck": (46.8083, -100.7837),
    "Columbus": (39.9612, -82.9988),
    "Oklahoma City": (35.4676, -97.5164),
    "Salem": (44.9429, -123.0351),
    "Harrisburg": (40.2732, -76.8867),
    "Providence": (41.824, -71.4128),
    "Columbia": (34.0007, -81.0348),
    "Pierre": (44.3683, -100.351),
    "Nashville": (36.1627, -86.7816),
    "Austin": (30.2672, -97.7431),
    "Salt Lake City": (40.7608, -111.891),
    "Montpelier": (44.2601, -72.5754),
    "Richmond": (37.5407, -77.436),
    "Olympia": (47.0379, -122.9007),
    "Charleston": (38.3498, -81.6326),
    "Madison": (43.0731, -89.4012),
    "Cheyenne": (41.1401, -104.8202),
}

# weatherMap icons look bad so i want to use my own
icon_map = {
    "01d": "https://cdn2.iconfinder.com/data/icons/weather-color-2/500/weather-01-1024.png", # clear
    "01n": "https://cdn2.iconfinder.com/data/icons/weather-color-2/500/weather-01-1024.png",
    "02d": "https://cdn2.iconfinder.com/data/icons/weather-color-2/500/weather-02-1024.png", # few clouds
    "02n": "https://cdn2.iconfinder.com/data/icons/weather-color-2/500/weather-02-1024.png",
    "03d": "https://cdn2.iconfinder.com/data/icons/weather-color-2/500/weather-02-1024.png", # scattered clouds
    "03n": "https://cdn2.iconfinder.com/data/icons/weather-color-2/500/weather-02-1024.png",
    "04d": "https://cdn2.iconfinder.com/data/icons/weather-color-2/500/weather-22-1024.png", # broken clouds
    "04n": "https://cdn2.iconfinder.com/data/icons/weather-color-2/500/weather-22-1024.png",
    "09d": "https://cdn2.iconfinder.com/data/icons/weather-color-2/500/weather-32-1024.png", # shower rain
    "09n": "https://cdn2.iconfinder.com/data/icons/weather-color-2/500/weather-32-1024.png",
    "10d": "https://cdn2.iconfinder.com/data/icons/weather-color-2/500/weather-32-1024.png", # rain
    "10n": "https://cdn2.iconfinder.com/data/icons/weather-color-2/500/weather-32-1024.png",
    "11d": "https://cdn2.iconfinder.com/data/icons/weather-color-2/500/weather-23-1024.png", # thunderstorm
    "11n": "https://cdn2.iconfinder.com/data/icons/weather-color-2/500/weather-23-1024.png",
    "13d": "https://cdn2.iconfinder.com/data/icons/weather-color-2/500/weather-24-1024.png", # snow
    "13n": "https://cdn2.iconfinder.com/data/icons/weather-color-2/500/weather-24-1024.png",
    "50d": "https://cdn2.iconfinder.com/data/icons/weather-color-2/500/weather-27-1024.png", # mist/fog
    "50n": "https://cdn2.iconfinder.com/data/icons/weather-color-2/500/weather-27-1024.png",
}


# build map
map = folium.Map(location=[44.0682, -114.742], zoom_start=7)

# create markers for each city
for city, (lat, lon) in cities.items():
    weather_url = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&units=imperial&appid={api_key}"

    # api call
    response = requests.get(weather_url)
    weather_data = response.json()

    # get weather data
    if "current" in weather_data:

        temp = weather_data["current"]["temp"]
        weather_type = weather_data["current"]["weather"][0]["description"]
        icon = weather_data["current"]["weather"][0]["icon"]


        # configure text and add a pretty image
        icon_url = icon_map[icon]
        popup_text = f"Temperature: {temp}°F<br>{weather_type.capitalize()}"


        # marker for image and popup
        folium.Marker(
            location=[lat - 0.01, lon], 
            popup=popup_text, 
            icon=folium.CustomIcon(icon_url, icon_size=(75, 75))
        ).add_to(map)

# put a title on screen
map.get_root().html.add_child(Element('<h3 align="center" style="font-size:20px;"><b>Weather Map of Idaho & Utah</b></h3>'))

map.get_root().html.add_child(Element("<title>Idaho and State Capital Weather</title>"))

map.save("rexburg_byui_map.html")