import os
import sys
import shutil
import requests
import json 
from dotenv import load_dotenv
import time
from colorama import Fore, Style

load_dotenv()

clientID = os.getenv("CLIENT_ID")
clientToken = os.getenv("CLIENT_TOKEN")
redditUsername = os.getenv("REDDIT_USERNAME")
accessToken = None

#======================================================

def generateToken():
    oAuthEndpoint = "https://www.reddit.com/api/v1/access_token"

    authData = {"grant_type" : "client_credentials"}
    authInfo = (clientID, clientToken)
    authHeader = {"user-agent" : f"dataCollector (by /u/{redditUsername})"}


    response = requests.post(url = oAuthEndpoint, data = authData, auth = authInfo, headers = authHeader)


    if (response.status_code == 200):
        global accessToken
        responseJSON = response.json()
        accessToken = responseJSON.get("access_token")

        print(Fore.GREEN +"Obtained and saved access token" + Style.RESET_ALL)
        

    else:
        print(Fore.RED +f"oAuth failed with status code: {response.status_code}" + Style.RESET_ALL)
        sys.exit()


#===========================


def risingPosts(subreddit, numPosts, numComments):
    subredditEndpoint = f"https://oauth.reddit.com/r/{subreddit}/rising"

    headers = {"Authorization": f"Bearer {accessToken}", "User-Agent": f"dataCollector:v1 (by /u/{redditUsername})"}
    params = {"limit": numPosts}
     

    response = requests.get(url = subredditEndpoint, headers = headers, params = params)


    if(response.status_code == 200):
        print(Fore.GREEN +f"Gathered {numPosts} threads from the subreddit r/{subreddit}" + Style.RESET_ALL)
        

        fileName = f"{subreddit}_RawData.json"
        data = response.json()


        for post in data["data"]["children"]:
            post_id = post["data"]["id"]
            post["data"]["comments"] = getComments(post_id, numComments, numPosts)

        print(Fore.GREEN + f"Fetched {numComments * numPosts} comments in total" + Style.RESET_ALL)
        

        savefile(data, fileName)
    
        

    else:
        print(Fore.RED +f"Fetching posts from {subreddit} failed with status code: {response.status_code}" + Style.RESET_ALL)
        sys.exit()


#===========================


def getComments(post_id, numComments, numPosts):
    commentEndpoint = f"https://oauth.reddit.com/comments/{post_id}"

    headers = {"Authorization": f"Bearer {accessToken}", "User-Agent": f"dataCollector:v1 (by /u/{redditUsername})"}
    params = {"limit": numComments}


    response = requests.get(url = commentEndpoint, headers = headers, params = params)


    if (response.status_code == 200):
        commentData = response.json()

        comments = []
        for comment in commentData[1]["data"]["children"]:
            if "body" in comment["data"]:  
                comments.append(comment)
    
    else:
        print(Fore.RED + f"Error occured while fetching comments with status code: {response.status_code}")
        print("="*50 + "\n")
        sys.exit()


    return comments

#===========================

def savefile(data, fileName):
    path = os.path.join("Data", fileName)

    time.sleep(1.5)

    with open(path, "w", encoding = "utf-8") as file:
        json.dump(obj = data, fp =  file, indent = 3)

        print(Fore.GREEN + f"Dumped data into {fileName}" + Style.RESET_ALL)
        print("="*50 + "\n")

        time.sleep(2)

#===========================
