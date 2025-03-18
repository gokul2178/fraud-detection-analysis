import sys
import os 
sys.dont_write_bytecode = True

from Data_Collection import *
from Data_Modification import *


filePath = os.path.realpath(__file__)
directory = os.path.dirname(filePath)
os.chdir(directory)



def main():
    print("")
    generateToken()
    
    risingPosts(subreddit = "Scams", numPosts = 5, numComments = 5)

    convertCSV()



if (__name__ == "__main__"):
    main()