import tkinter as tk
import customtkinter as ctk
from dotenv import load_dotenv
from requests import get
from os import getenv
from json import loads
from PIL import Image

load_dotenv()

class Window:
    # window object
    def __init__(self,_title,height,width):
        self.__root = ctk.CTk()    # initializing window
        self.__root.title(_title)
        self.__root.geometry(f"{height}x{width}")
        self.__root.minsize(height,width)
        self.__root.maxsize(height,width)
        
    @property
    def root(self):
        return self.__root

    def setMode(self, mode=-1):
        if mode == 0:
            ctk.set_appearance_mode("White")
        elif mode == 1:
            ctk.set_appearance_mode("Dark")
        else:
            ctk.set_appearance_mode("System")
        return

    
def weatherSearch(root):
    [_height, caller] = [46, lambda: fetchData(root, search_entry.get())]
    search_entry = ctk.CTkEntry(
      root, placeholder_text="search a location",height=_height,
      width=310,font=('sans-serif', 18)
    )
    search_button = ctk.CTkButton(
      root,text="search",height=_height-2,width=_height,font=('sans-serif',17),
      fg_color='red',command=caller
    )
    search_entry.grid(padx=4,pady=4)
    search_button.grid(padx=5,pady=5)
    search_entry.place(relx=0.47,rely=0.05,anchor=tk.CENTER)    
    search_button.place(relx=0.7,rely=0.05,anchor=tk.CENTER)
    return

def weatherIcon(root,condition):
    image = "/"
    if condition == "Sunny" or condition == "Clear":
        image = "assets/clear.jpeg"
    elif condition == "Partly cloudy" or condition == "Partly Clear":
        image = "assets/partly_cloudy.png"
    elif condition == "Fog" or condition == "Mist":
        image = "assets/fog.png"
    elif condition == "Cloudy" or condition == "Overcast":
        image = "assets/cloud.jpeg"
    open_image = Image.open(image)
    load_image = ctk.CTkImage(light_image=open_image,dark_image=open_image,size=(140,140))
    image_label = ctk.CTkLabel(root,text="",image=load_image)
    image_label.pack(pady=10)
    image_label.place(relx=0.75,rely=0.5,anchor=tk.CENTER)
    return

def renderCityDetails(root, content):
    cityname,latlong = (ctk.CTkLabel(
      root,text=f"{content['name']},{content['country']}",font=('sans-serif',27)
    ),ctk.CTkLabel(
      root,text=f"{round(content['lat'],2)} {round(content['lon'],2)}",
      font=('monospace',26),text_color="#1c1d1f"    
    ))
    cityname.grid(padx=6,pady=6)
    latlong.grid(padx=6,pady=6)
    cityname.place(relx=0.31,rely=0.2,anchor=tk.CENTER)
    latlong.place(relx=0.59,rely=0.2,anchor=tk.CENTER)
    return

def renderWeather(root, content):
    (temperature,visibility_km,cloud_coverage,weather_text) = (ctk.CTkLabel(
      root,text=f"{content['temp_c']} *C",font=('calbri',65, "bold"),
      text_color="#000"
    ),ctk.CTkLabel(
      root,text=f"visibility - {content['vis_km']} km",font=('calbri',22),
      text_color="#111"
    ),ctk.CTkLabel(
      root,text=f"cloud coverage - {content['cloud']}%",font=('calbri',22),
      text_color="#111"        
    ),ctk.CTkLabel(root,text=f"{content['condition']['text']}",font=('calbri',27,"bold"),
      text_color="#333"
    ))
    humidity_text = ctk.CTkLabel(
      root,text=f"wind speed - {content['wind_kph']} km/h",font=('calbri',22),
      text_color="#111"
    ) 
    visibility_km.grid(padx=5,pady=5)
    temperature.grid(padx=5,pady=5)
    cloud_coverage.grid(padx=5,pady=5)
    weather_text.grid(padx=5,pady=5)
    humidity_text.grid(padx=3,pady=3)
    visibility_km.place(relx=0.2,rely=0.48,anchor=tk.CENTER)
    temperature.place(relx=0.2,rely=0.4,anchor=tk.CENTER)
    cloud_coverage.place(relx=0.2,rely=0.52,anchor=tk.CENTER)
    weather_text.place(relx=0.75,rely=0.37,anchor=tk.CENTER)
    humidity_text.place(relx=0.21,rely=0.57,anchor=tk.CENTER)
    weatherIcon(root, content['condition']['text'])
    return
 
def fetchData(root, _query):  
    try:
        # if string is empty then throw an exception
        if "".join(_query.split()) == '':
            raise Exception
        request = get(f"http://api.weatherapi.com/v1/forecast.json?key={getenv("API_KEY")}&q={_query}&days=4&aqi=no&alerts=no")
        if not request.ok:
            if request.status_code == 400 or request.status_code == 404:
                raise Exception
            if request.status_code == 408 or request.status_code == 503:
                raise ConnectionError("Request timed out, try again later")
            raise Exception
        parsed = loads(request.text)
        renderCityDetails(root, parsed['location'])
        renderWeather(root, parsed['current'])
    except Exception:
        text_label = ctk.CTkLabel(root,text="invalid input! try again",font=('sans-serif',33),text_color='red')
        text_label.place(relx=0.5,rely=0.5,anchor=tk.CENTER)
    except ConnectionError as e:
        text_label = ctk.CTkLabel(root,text=e,font=('sans-serif',33),text_color="red")
        text_label.place(relx=0.5,rely=0.5,anchor=tk.CENTER)
    return

def main():
    app = Window("Beautiful Weather Lookup", 850,650)
    root = app.root
    weatherSearch(root)
    root.mainloop()
    return

if __name__ == "__main__":
    main()
