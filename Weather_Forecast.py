import requests
import PIL
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import messagebox
import os

weather_icon = {
    "clear sky": "clear.png",
    "few clouds": "partcloud.png",
    "scattered clouds": "cloudy.png",
    "broken clouds": "cloudy.png",
    "overcast clouds": "cloudy.png",
    "light rain": "rain.png",
    "moderate rain": "rain.png",
    "heavy rain": "rain.png",
    "thunderstorm": "storm.png",
    "snow": "snow.png",
    "mist": "mist.png",
    "fog": "mist.png",
    "haze": "haze.png",

}

# Default color themes
themes = {
    "light": {
        "bg": "#add8e6",
        "fg": "black",
        "button_bg": "#d81e1e",
        "button_fg": "white"
    },
    "dark": {
        "bg": "#1e1e1e",
        "fg": "white",
        "button_bg": "#101d82",
        "button_fg": "white"
    }
}

current_theme = "light"  # Default theme

def apply_theme():
    theme = themes[current_theme]
    root.configure(bg=theme["bg"])
    for widget in root.winfo_children():
        if isinstance(widget, (tk.Label, tk.Button, tk.Entry)):
            widget.configure(bg=theme["bg"], fg=theme["fg"])
        if isinstance(widget, tk.Button):
            widget.configure(bg=theme["button_bg"], fg=theme["button_fg"])
    result_label.configure(bg=theme["bg"], fg=theme["fg"])
    icon_label.configure(bg=theme["bg"])

def toggle_theme():
    global current_theme
    current_theme = "dark" if current_theme == "light" else "light"
    apply_theme()

api_key = "dbd27a127e826fa1db436714a7ff1192"

def get_weather():
    city = city_entry.get()
    if city == "":
        messagebox.showerror("Error", "Please enter a city name.")
        return
    

    url= "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"  #celisius
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        if response.status_code == 200:
                    data = response.json()
                    temperature = data["main"]["temp"]
                    description = data["weather"][0]["description"].strip().lower()
                    humidity = data["main"]["humidity"]
                    wind_speed = data["wind"]["speed"]

                    result_label.config(
                         text=f"\n📍 Weather in {city}:\n🌡️ Temperature: {temperature}°C\n🌧️ Condition: {description}\n💧 Humidity: {humidity}%\n 🌬️ Wind Speed: {wind_speed} m/s"
                    )
    

        # get corresponding weather icon
        base_dir = os.path.dirname(os.path.abspath(__file__))
        icon_name = weather_icon.get(description, "default.png")
        icon_path = os.path.join(base_dir, "icons", icon_name)


        print(f"Description: '{description}'")
        print(f"Using icon: {icon_path}")
        

        if os.path.exists(icon_path):
            icon_image = Image.open(icon_path)
            icon_image = icon_image.resize((100, 100),  Image.Resampling.LANCZOS)
            icon_photo = ImageTk.PhotoImage(icon_image)
            icon_label.config(image=icon_photo)
            icon_label.image = icon_photo
        else:
            print("⚠️ Icon not found. Showing blank.")
            icon_label.config(image="")
            icon_label.image = None
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Error fetching weather data: {e}")
        return
    
# GUI code
root = tk.Tk()
root.title("Weather Forecast")
root.geometry("400x400")
root.resizable(False, False)
root.configure(bg="#f4a2eb")

tk.Label(root, text="Weather Forecast", font=("Helvetica", 24, "bold"), bg="#f4a2eb").pack(pady=20)
city_label = tk.Label(root, text="Enter city name:")
city_label.pack()

theme_button = tk.Button(root, text="🌙Toggle Theme", command=toggle_theme)
theme_button.place(relx=0.5, y=12, anchor='center')

city_entry = tk.Entry(root)
city_entry.pack()

search_button = tk.Button(root, text="Search", command=get_weather)
search_button.pack()

result_label = tk.Label(root, text="")
result_label.pack()

icon_label = tk.Label(root, bg=themes[current_theme]["bg"])
icon_label.pack(pady=(10,0))

apply_theme()  # Apply the default theme
root.mainloop()

