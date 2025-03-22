import sys
import os 
sys.dont_write_bytecode = True

from Data_Collection import *
from Data_Modification import *


filePath = os.path.realpath(__file__)
directory = os.path.dirname(filePath)
os.chdir(directory)


if os.path.exists:
    shutil.rmtree("Data")
    os.mkdir("Data")
else: 
    os.mkdir("Data")

#======================================================

def main():
    print("")

    generateToken()
    
    risingPosts(subreddit = "Scams", numPosts = 3, numComments = 3)

    convertCSV()



if (__name__ == "__main__"):
    main()
