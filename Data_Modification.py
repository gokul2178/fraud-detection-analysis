import os
import pandas as pd
import json


def convertCSV():
    dirPath = os.path.dirname(__file__)
    os.path.join(dirPath, "Data")
    os.chdir(dirPath)
    data_path = os.path.join(os.getcwd(), "Data")


    fileNames = []
    for file in os.listdir(data_path):
        if (file.endswith(".json")):
            fileNames.append(file)
            

    dataframes = []
    for file in fileNames:
        filePath = os.path.join("Data", file)

        with open(filePath, "r", encoding = "utf-8") as fileObj:
            dataJSON = json.load(fileObj)

            df = pd.json_normalize(data = dataJSON["data"]["children"])
            df = df[["data.subreddit", "data.title", "data.selftext", "data.author", "data.ups"]]

            dataframes.append(df)


    print(df)

def cleanData():
    pass