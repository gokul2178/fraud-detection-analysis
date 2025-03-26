import os
import re
import pandas as pd
import json
import time
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from colorama import Fore, Style

#Avoids installing message everytime you run
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)


os.chdir(os.getcwd())

pd.set_option('display.max_colwidth', None)

dirPath = os.path.dirname(__file__)
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
    print(Fore.GREEN + "\nModifying Data.." + Style.RESET_ALL)
    os.chdir(os.path.join(os.getcwd(), "Data"))


    #Read all the csv files into a dataframe
    dataframes = []
    for file in os.listdir():
        if(file.endswith(".csv")):
            path = os.path.join(os.getcwd(), file)
            df = pd.read_csv(file)
            dataframes.append(df)

    #Create 1 dataframe with all the threads from all CSV files
    df = pd.concat(dataframes)
    df = df.reset_index(drop = True)



    #Rename columns and create new column with all text information
    df = df.rename(columns = {"data.subreddit":"Subreddit", "data.author":"Author", "data.title":"Title", "data.selftext":"Subheading", "data.ups":"Upvotes", "data.comments":"Comments"})
    df["Content"] = df["Title"] + " " + df["Subheading"] + " " + df["Comments"]

    #Filter out to keep only text
    phrase = r"\(https:[^\)]+\) | /u/\S+ | \\n|[^\w\s] | [0-9]"
    df["Content"] = df["Content"].apply(lambda x: re.sub(phrase, " ", str(x)))
    df["Content"] = df["Content"].str.lower()

    #Tokenization
    df["Content"] = df["Content"].str.split()
    stopWords = set(stopwords.words("english"))

    #Lemmantize words
    lemmatizer = WordNetLemmatizer()
    df["Content"] = df["Content"].apply(lambda row: " ".join(lemmatizer.lemmatize(word) for word in row))

    #Remove stop-words
    df["Content"] = df["Content"].apply(lambda row: " ".join(word for word in row.split() if word not in stopWords))

    df = df.rename(columns = {"Content":"cleanContent"})

    

    
    df = createRiskInfo(df)
    print(Fore.GREEN + "Cleaned Data" + Style.RESET_ALL)


#===========================


def createRiskInfo(df):

    def wordDetector(row):
        keywords = ["identity theft", "fraud", "financial fraud", "money laundering", "wire fraud", 
        "credit card fraud", "bank fraud", "phishing", "Ponzi", "pyramid scheme",
        "scam", "counterfeit", "fraudulent", "unauthorized transactions", "fraud alert", 
        "hacking", "hacked", "data breach", "malware", "phishing email", "impersonation", 
        "bribery", "blackmail", "social engineering", "deception", "hoax", "cheat",
        "phishing website", "tech support", "employment fraud", "job offer", "job", 
        "credit card", "fraudulent charges", "chargeback", "password", "passcode", "insider fraud", 
        "NFT", "fake check", "invest", "deposit", "fee", "lottery", "email", "pump and dump", 
        "forex", "package", "donation", "warranty", "data", "misleading", "deceptive marketing"]
            
        foundKeywords = [word for word in keywords if word in row]
        wordList = ", ".join(foundKeywords)
        return wordList



    df["Keywords"] = df["cleanContent"].apply(wordDetector)



    #print(df["Keywords"])  

