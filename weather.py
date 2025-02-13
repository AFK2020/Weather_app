import requests, json
import functools
import time
import datetime
from datetime import date, timedelta
from datetime import datetime
import matplotlib.pyplot as plt
import csv
import pandas as pd
from csv import writer
import argparse


def pipeline(start_dt,end_dt):

    start=(start_dt)
    end=(end_dt)
    delta = timedelta(days=1)

    graph_list=[]
    csv_list=[]
    dates = []
    file_path="Data.csv"

    while start <= end:
        # add current date to list by converting  it to iso format
        dates.append(start.strftime("%Y-%m-%d"))
        # increment start date by timedelta
        start += delta

    for dt in dates:
        result=fetch_data(dt)
        dict_data=extract_save_data(result,file_path)
        graph_list.append(dict_data)

    



def plot_graph(lst):

    for i in range(len(lst+1)):
        plt.plot(lst[0]["Date"],lst[0]["Minimum Temperature"])




def retry(func):
    pass

def fetch_data(start_date):

    start_date=str(start_date)

    try:
        weatherAPI=f"https://archive-api.open-meteo.com/v1/archive?latitude=52.52&longitude=13.41&start_date={start_date}&end_date={start_date}&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m,soil_temperature_0_to_7cm&timezone=GMT"

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
        

        if temprature< min_temp:
            min_temp=temprature

        if soil_temp>max_soil_temp:
            max_soil_temp=soil_temp
        
        if soil_temp<min_soil_temp:

            min_soil_temp=soil_temp

        if windspeed>max_wind_speed:
            max_wind_speed=windspeed
        
        if windspeed<min_wind_speed:
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

    dict2={
        "Date": time,
        "Minimum Temperature": min_temp,
        "Maximum Temperature": max_temp,
        "Avergae Temperature" : temp_sum/count,
        "Minimum Windspeed": min_wind_speed,
        "Maximum Windspeed": max_wind_speed,
        "Avergae Temperature" : wind_speed_sum/count,
        "Minimum Soil Temperature": min_soil_temp,
        "Maximum Soil Temperature" : max_soil_temp,
        "Average Soil Temperature" : soil_temp_sum/count
    }


    return dict2







if __name__ == "__main__":

    parser=argparse.ArgumentParser()    #create parse object

    parser.add_argument("Start_date", type=str , help="Start and end date in format YYYY-MM_DD")
    parser.add_argument("End_date", type=str , help="Start and end date in format YYYY-MM_DD")

    args=parser.parse_args()
    start_date = datetime.strptime(args.Start_date, "%Y-%m-%d")
    end_date = datetime.strptime(args.End_date, "%Y-%m-%d")



    pipeline(start_date,end_date)
    # your function here

