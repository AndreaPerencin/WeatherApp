import csv
from csv import writer
import requests
from datetime import datetime



string_req_daily = "https://api.open-meteo.com/v1/forecast?latitude={#MY-LATITUDE#}&longitude={#MY-LONGITUDE#}&daily=temperature_2m_max,temperature_2m_min,sunrise,sunset,precipitation_sum,precipitation_probability_max,wind_speed_10m_max,sunshine_duration&timezone=Europe%2FLondon"

string_req_detailed = "https://api.open-meteo.com/v1/forecast?latitude={#MY-LATITUDE#}&longitude={#MY-LONGITUDE#}&hourly=temperature_2m,precipitation,precipitation_probability,wind_speed_10m,cloud_cover&forecast_days=2"



print(f"\n{" ***** WEATHER APP *****":^40}")


def readCities():
    data_dict = {}
    with open("cities.csv", mode="r") as csvfile:
        csv_info = csv.DictReader(csvfile)
        
        for row in csv_info:
            key = row["city"].lower()
            data_dict[key] = row["lat"],row["lng"]
    return data_dict
            

def appendCity(cityTyped, lat_usr, long_usr, data_dict):
    cityTyped = cityTyped.lower()
    data_dict.update({cityTyped:(str(lat_usr),str(long_usr))})
    with open("cities.csv", mode="a") as csvfile:
        csv_info = writer(csvfile)
        csv_info.writerow([cityTyped, lat_usr,long_usr])
        csvfile.close() 




            
def mainMenu(data_dict):        
    while True:    
        choice_menu = input("""
Please select:
s) See forecast
a) Add a new city
d) Delete a city
l) See full list
x) Exit
""").lower()

        while choice_menu not in ["s","a","d","l","x"]:
              choice_menu = input("Invalid choice, please try again :").lower()

        if choice_menu =="s":
            selectCity(data_dict)
        elif choice_menu =="a":
            nameCity = input("Please enter the city name or press 0 to go back: ")
            if nameCity != '0':
                addCity(nameCity, data_dict)
            else:
                pass
        elif choice_menu =="d":
            deleteCity(data_dict)
        elif choice_menu =="l":
            listCity(data_dict)
        elif choice_menu =="x":
            break
        
        
def selectCity(data_dict):
    cityTyped = input("Please type the name of the city: ").lower()
    if cityTyped not in data_dict:
        theChoice = input(f"{cityTyped} is not in the database. Do you want to add it? [Y/N] ").lower()
        if theChoice == "y":
            addCity(cityTyped,data_dict)
        else:
            print("...Back to main menu\n")
            return
    else:
        forecastType = input("What kind of forecast do you want to see?\nw) Forecast for next week\nd) Detailed forecast for today and tomorrow\n").lower()
        if forecastType== "w":
            dailyForecast(cityTyped,data_dict)
        elif forecastType== "d":
            detailedForecast(cityTyped,data_dict)
        else:
            input("Invalid choice\n...Back to main menu\n")
            return            
        
    
    
    
def dailyForecast(cityTyped,data_dict):      
    latitude = data_dict[cityTyped][0]
    longitude = data_dict[cityTyped][1]
    string_req_daily_workings = string_req_daily.replace("{#MY-LATITUDE#}",str(latitude))
    string_req_daily_workings = string_req_daily_workings.replace("{#MY-LONGITUDE#}",str(longitude))
    result=requests.get(string_req_daily_workings)
    all_data = result.json()
    daily_data = list(all_data.values())[8]
    
    daysList = daily_data['time']
    tempMaxList = daily_data['temperature_2m_max']
    tempMinList = daily_data['temperature_2m_min']
    sunriseList = daily_data['sunrise']
    sunsetList = daily_data['sunset']
    precSumList = daily_data['precipitation_sum']
    precProbList = daily_data['precipitation_probability_max']
    windSpeedList = daily_data['wind_speed_10m_max']
    sunDurationList = daily_data['sunshine_duration']
    
    print("\n----Forecast for next week----")
    for x in range(0,6):
        print()
        currentday_datetime = datetime.strptime(daysList[x], "%Y-%m-%d")
        currentday = currentday_datetime.strftime("%d-%m-%Y")
        print("DAY: ", currentday)
        print(f"Max temperature is {tempMaxList[x]} and min temperature is {tempMinList[x]}")
        print(f"Probabily of precipitation is {precProbList[x]}% ({precSumList[x]}mm)")
        sunshineMinutes = int((sunDurationList[x])/60)
        if sunshineMinutes>60:
            sunshineOutput = str(int(sunshineMinutes/60))+" hours"
        else:
            sunshineOutput = str(sunshineMinutes)+" minutes"
        print(f"Sunrise at {sunriseList[x][-5:]} and sunset at {sunsetList[x][-5:]}. Sunshine duration is {sunshineOutput}")
        print(f"Wind speed is {windSpeedList[x]} km/h") 
    input("\nPress any key to return to the main menu...") 


def detailedForecast(cityTyped,data_dict):
    latitude = data_dict[cityTyped][0]
    longitude = data_dict[cityTyped][1]
    string_req_detailed_workings = string_req_detailed.replace("{#MY-LATITUDE#}",str(latitude))
    string_req_detailed_workings = string_req_detailed_workings.replace("{#MY-LONGITUDE#}",str(longitude))
    result=requests.get(string_req_detailed_workings)
    all_data = result.json()
    daily_data = list(all_data.values())[8]
    
    timeList = daily_data['time']
    tempList = daily_data['temperature_2m']
    precList = daily_data['precipitation']
    precProbList = daily_data['precipitation_probability']
    windSpeedList = daily_data['wind_speed_10m']
    cloudCoverList = daily_data['cloud_cover']
    
    print("      TIME         TEMPERATURE   PRECIPITATION_PROB_%     PRECIPITATION_MM      WINDSPEED_KM/H         CLOUD_COVER_%")
    
    for x in range(0,len(timeList)): 
        correctDate = datetime.strptime(timeList[x][:10], "%Y-%m-%d")
        currentDate = correctDate.strftime("%d-%m-%Y")
        dateTimeOk = currentDate+"@"+timeList[x][-5:]
        print(f"{dateTimeOk}     {tempList[x]:>6}   {precProbList[x]:>14}             {precList[x]:>10}            {windSpeedList[x]:>10}            {cloudCoverList[x]:>10}")
    input("\nPress any key to return to the main menu...")




def addCity(cityTyped,data_dict):
    lat_usr = 500
    long_usr = 500
    
    while abs(lat_usr) > 90:
        lat_usr = round(float(input("Latitude: ")),2)
    
    while abs(long_usr) > 180:
        long_usr = round(float(input("Longitude :")),2)
        
    choice = input(f"The new location is {cityTyped} and had latitude {lat_usr} and longitude {long_usr}\nAre those details correct? [Y/N]").lower()
    if(choice == "y"):
        appendCity(cityTyped, lat_usr, long_usr, data_dict)
    else:
        print("Changes discarded")
        input("\nPress any key to return to the main menu...")


def deleteCity(data_dict):
    city_to_delete = input("Please type the name of the city you want to delete: ").lower()
    if city_to_delete in data_dict.keys():
        confirmation = input(f"Do you really want to delete {city_to_delete}? [y/n]").lower()
        if confirmation == "y":
            del data_dict[city_to_delete]
            with open("cities.csv", mode="w") as csvfile:
                csv_info = writer(csvfile)
                csv_info.writerow(["city","lat","lng"])
                
                for key,(lat,lng) in data_dict.items():
                    csv_info.writerow([key,lat,lng])
                csvfile.close() 
        else:
            input("Operation cancelled.\nPress any key to return to the main menu...")
    else:
        input(f"{city_to_delete} not found\nPress any key to return to the main menu...")



def listCity(data_dict):
    print("CITY  : (LATITUDE, LONGITUDE)")
    for key, value in data_dict.items():
        print(f"{key}: {value}")
    input("\nPress any key to return to the main menu...")



mainMenu(readCities())
