import requests
import json
import sqlite3
from win10toast import ToastNotifier


api_key = "YOUR_API_KEY"
city = "New York"
url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"


def get_weather_data(url):
    response = requests.get(url)
    return response.json()


weather_data = get_weather_data(url)


with open("weather_data.json", "w") as json_file:
    json.dump(weather_data, json_file, indent=4)


def print_weather_info(data):
    print("Weather Information:")
    print(f"City: {data['name']}")
    print(f"Temperature: {data['main']['temp']} K")
    print(f"Description: {data['weather'][0]['description']}")
    print(f"Humidity: {data['main']['humidity']}%")
    print(f"Wind Speed: {data['wind']['speed']} m/s")


print_weather_info(weather_data)


conn = sqlite3.connect("weather.db")
cursor = conn.cursor()


cursor.execute("CREATE TABLE IF NOT EXISTS weather (city TEXT, temperature REAL, description TEXT, humidity REAL, wind_speed REAL)")


cursor.execute("INSERT INTO weather VALUES (?, ?, ?, ?, ?)",
               (weather_data["name"], weather_data["main"]["temp"],
                weather_data["weather"][0]["description"], weather_data["main"]["humidity"],
                weather_data["wind"]["speed"]))


conn.commit()
conn.close()


toaster = ToastNotifier()
notification_text = f"Weather in {weather_data['name']}:\nTemperature: {weather_data['main']['temp']} K\nDescription: {weather_data['weather'][0]['description']}"
toaster.show_toast("Weather Notification", notification_text, duration=10)