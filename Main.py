import sys
import os
import shutil
sys.dont_write_bytecode = True

from Data_Collection import *
from Data_Modification import *

filePath = os.path.realpath(__file__)
directory = os.path.dirname(filePath)
os.chdir(directory)


if os.path.exists("Data"):
    shutil.rmtree("Data")
    os.mkdir("Data")
else: 
    os.mkdir("Data")

#======================================================

def main():
    
    print("")

    generateToken()
    
    
    # Can call more functions here to get more posts
    risingPosts(subreddit = "Scams", numPosts = 15, numComments = 4)
    #risingPosts(subreddit = "scammers", numPosts = 25, numComments = 3)


    convertCSV()   
    df = cleanData()
    df.to_csv("cleanData.csv") 


    print(Fore.GREEN + "Cleaned data and saved as CSV" + Style.RESET_ALL)
    time.sleep(1)
    exit()

if (__name__ == "__main__"):
    main()
