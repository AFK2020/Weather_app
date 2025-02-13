import requests, json
import functools
import time
import datetime
from datetime import date, timedelta
from datetime import datetime
import matplotlib.pyplot as plt
import csv
from csv import writer
import argparse
from utils import retry
from utils import csv_write
from utils import plot_graph


def pipeline(start,end):

    delta = timedelta(days=1)
    dates = []


    graph_list=[]
    csv_lst=[]
    file_path="Data.csv"

    while start <= end:
        dates.append(start.strftime("%Y-%m-%d"))
        #dates.append(start.date())
        start += delta

    for dt in dates:
        result=fetch_data(dt)
        dict_data=extract_save_data(result)
        graph_list.append(dict_data[0])
        csv_lst.append(dict_data[1])

    csv_write(csv_lst,file_path)

    plot_graph(graph_list)



    

@retry
def fetch_data(start_date):

    start_date=str(start_date)
    http_url="https://archive-api.open-meteo.com/v1/archive"
    try:
        weatherAPI=f"{http_url}?latitude=52.52&longitude=13.41&start_date={start_date}&end_date={start_date}&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m,soil_temperature_0_to_7cm&timezone=GMT"

        response=requests.get(weatherAPI)
        #print(response)
        response.raise_for_status()
        data=response.json()
        #print(data["hourly"]["temperature_2m"][1])
        return data
    
    except requests.RequestException as e:
        print("Error fetching data", e)
        return None

    


def extract_save_data(result):

    count=0

    lst_dict=[]
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

        lst_dict.append(dictionary)

    dict2={
        "Date": time,
        "Minimum_Temperature": min_temp,
        "Maximum_Temperature": max_temp,
        "Avergae_Temperature" : temp_sum/count,
        "Minimum_Windspeed": min_wind_speed,
        "Maximum_Windspeed": max_wind_speed,
        "Avergae_Temperature" : wind_speed_sum/count,
        "Minimum_Soil_Temperature": min_soil_temp,
        "Maximum_Soil_Temperature" : max_soil_temp,
        "Average_Soil_Temperature" : soil_temp_sum/count
    }


    return dict2,lst_dict



if __name__ == "__main__":

    parser=argparse.ArgumentParser()    #create parse object

    parser.add_argument("Start_date", type=str , help="Start and end date in format YYYY-MM_DD")
    parser.add_argument("End_date", type=str , help="Start and end date in format YYYY-MM_DD")

    args=parser.parse_args()
    start_date = datetime.strptime(args.Start_date, "%Y-%m-%d")
    end_date = datetime.strptime(args.End_date, "%Y-%m-%d")




    pipeline(start_date,end_date)
    # your function here

