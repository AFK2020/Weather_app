import requests, json
import functools
import time
import datetime
import csv
from csv import writer
import argparse







def retry(func):
    pass

def fetch_data():

    try:
        weatherAPI="https://archive-api.open-meteo.com/v1/archive?latitude=52.52&longitude=13.41&start_date=2025-01-01&end_date=2025-01-03&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m,soil_temperature_0_to_7cm&timezone=GMT"

        response=requests.get(weatherAPI)
        #print(response)
        response.raise_for_status()
        data=response.json()
        #print(data["hourly"]["temperature_2m"][1])
        return data
    
    except requests.RequestException as e:
        print("Error fetching data", e)
        return None

    


def extract_save_data(result,file_path):

    count=0

    min_temp = float('inf')
    max_temp = float('-inf')
    min_soil_temp = float('inf')
    max_soil_temp = float('-inf')
    min_wind_speed = float('inf')
    max_wind_speed = float('-inf')
    temp_sum=soil_temp_sum=wind_speed_sum=0


    for i in range(len(result["hourly"]["time"])):
        time= result["hourly"]["time"][i]
        temprature = result["hourly"]["temperature_2m"][i]
        soil_temp =result["hourly"]["soil_temperature_0_to_7cm"][i]
        windspeed =result["hourly"]["wind_speed_10m"][i]
        count+=1


        temp_sum+=temprature
        wind_speed_sum +=windspeed
        soil_temp_sum+=soil_temp

        if temprature>max_temp:
            max_temp=temprature
            max_date=time
        

        elif temprature< min_temp:
            min_temp=temprature
            min_time=time

        if soil_temp>max_soil_temp:
            max_soil_temp=soil_temp
        
        elif soil_temp<min_soil_temp:

            min_soil_temp=soil_temp

        if windspeed>max_wind_speed:
            max_wind_speed=windspeed
        
        elif windspeed<min_wind_speed:
            min_wind_speed= windspeed    




        dictionary={

            "Date" : time,
            "temprature" : temprature,
            "soil_temprature": soil_temp,
            "windspeed" : windspeed


        }

        try:
        # Try to open the file in read mode
            with open(file_path, 'r', newline='', encoding='utf-8'):
                file_exists = True
        except FileNotFoundError:
            # If file doesn't exist, it will raise an error, so set file_exists to False
            file_exists = False


        if file_exists:
            # If the file exists, append to it
            with open(file_path, 'a', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=dictionary.keys())
                writer.writerow(dictionary)
        else:
            # If the file doesn't exist, create it and write the data
            with open(file_path, 'w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=dictionary.keys())
                writer.writeheader()  # Write the header. The key values are the headers
                writer.writerow(dictionary)  # Write the first row of data
    

    print(f"Minimum Temp=",min_temp,"C at Date",{min_time},"\nMaximum Temp", max_temp,"C at Date", {max_date})
    print(f"Minimum windspeed=",min_wind_speed,"\nMaximum windspeed", max_wind_speed)
    print(f"Minimum soil Temperature=",min_soil_temp,"\nMaximum soil Temperature", max_soil_temp)
    print(f"Avergae Temperature=",temp_sum/count)
    print(f"Avergae windspeed=",wind_speed_sum/count)
    print(f"Avergae Soil Temp=",soil_temp_sum/count)










result=fetch_data()

file_path="Data.csv"

total_count=extract_save_data(result,file_path)






# if __name__ == "__main__":

#     parser=argparse.ArgumentParser()    #create parse object

#     parser.add_argument("Start_date", "end_date", type=str ,  help="Start and end date in format YYYY-MM_DD")
#     # your function here

