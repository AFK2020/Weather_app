import functools
import time
from datetime import date, timedelta
from datetime import datetime
import matplotlib.pyplot as plt
import csv
from csv import writer



def retry(func, retries=3):

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        attemps=0

        while attemps<retries:
            try:
                return func(*args,*kwargs)
            except ConnectionError as e:
                print(e)
                time.sleep(2)
                attemps+=1

        print("Max retries reached. Exiting.")
        raise Exception(f"Failed to execute {func.__name__} after {retries} retries.")
    
    return wrapper




def plot_graph(lst):


    dates = [element["Date"][:10] for element in lst]        #one line for loop 
    min_temps= [element["Minimum_Temperature"] for element in lst]
    
    max_temps= [element["Maximum_Temperature"] for element in lst]
    min_ws= [element["Minimum_Windspeed"] for element in lst]
    max_ws=[element["Maximum_Windspeed"] for element in lst]
    min_st=[element["Minimum_Soil_Temperature"] for element in lst]
    max_st=[element["Maximum_Temperature"] for element in lst]
    avg_temp=[element["Average_Temperature"] for element in lst]
    avg_wd=[element["Average_Windspeed"] for element in lst]
    avg_st=[element["Average_Soil_Temperature"] for element in lst]




    plt.plot(dates,min_temps, label= "Min Temp")
    plt.plot(dates,max_temps, label= "Min Temp")
    plt.plot(dates,min_ws, label= "Min windspeed")
    plt.plot(dates,max_ws, label= "Max windspeed")
    plt.plot(dates,min_st, label= "Min Soil Temp")
    plt.plot(dates,max_st, label= "Max Soil Temp")
    plt.legend()


    plt.xticks(rotation=45, ha='right')

    plt.title("Weather values Vs Date")

    plt.xlabel("Date")


    plt.show()



def csv_write(csv_list,file_path):

    all_data_to_write = [item for sublist in csv_list for item in sublist]  # Flatten the list
    keys = all_data_to_write[0].keys()

    with open(file_path, 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        dict_writer.writeheader()  # Write the header
        dict_writer.writerows(all_data_to_write)  # Write all rows



