import os
import pandas as pd
import json
import time
from colorama import Fore, Style

pd.set_option('display.max_colwidth', None)

dirPath = os.path.dirname(__file__)
os.path.join(dirPath, "Data")
os.chdir(dirPath)

#======================================================

def convertCSV():
    data_path = os.path.join(os.getcwd(), "Data")


    fileNames = []
    for file in os.listdir(data_path):
        if (file.endswith(".json")):
            fileNames.append(file)
            

    dataframes = []
    for file in fileNames:
        filePath = os.path.join("Data", file)     
        name, ect = file.split("_")
        

        with open(filePath, "r", encoding = "utf-8") as fileObj:
            dataJSON = json.load(fileObj)

            
            df = pd.json_normalize(data = dataJSON["data"]["children"])
            df = df[["data.subreddit", "data.author", "data.title", "data.selftext", "data.ups", "data.comments"]]

            df["data.comments"] = df["data.comments"].apply(lambda keys: [x["data"]["body"] for x in keys])

            dataframes.append(df)

            df.to_csv(path_or_buf = os.path.join("Data", f"{name}_Data.csv"), index = False)
            time.sleep(1)
            

    print(Fore.BLUE + "Converted all JSON files to CSV" + Style.RESET_ALL)


#===========================


def cleanData():
    dataframes = []
    for file in os.listdir("Data"):
        if(file.endswith(".csv")):
            path = os.path.join("Data", file)
            df = pd.read_csv(path)
            dataframes.append(df)
        
    df = pd.concat(objs = dataframes)

    print(df) 

cleanData()
