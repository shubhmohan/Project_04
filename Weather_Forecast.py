import requests\

api_key = "dbd27a127e826fa1db436714a7ff1192"

def get_weather(city):
    url= "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"  #celisius
    }
    response = requests.get(url, params=params)
 


    if response.status_code == 200:
        data = response.json()
        temperature = data["main"]["temp"]
        description = data["weather"][0]["description"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]
        print(f"\n📍 Weather in {city}:\n🌡️ Temperature: {temperature}°C\n🌧️ Condition: {description}\n💧 Humidity: {humidity}%\n 🌬️ Wind Speed: {wind_speed}")

    else:
        return "Error fetching weather data."
    

city = input("Enter the city name: ")
print(get_weather(city))

