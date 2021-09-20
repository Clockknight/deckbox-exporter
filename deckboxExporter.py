import os
import sys
import csv

print("Please enter the directory of the file you want to convert.")
print("NOTE: PLEASE make sure to follow the readMe instructions!")
nameLib = {}
editLib = {}
condLib = {}
rariLib = {}
deckboxDir = input("\t")

#Quick validation if else
if not os.path.isfile(deckboxDir) or deckboxDir[-4:] != ".csv":
    print(deckboxDir[:-4])
    print("Sorry, that path isn't valid!")
    sys.exit()
else:
    #Making a file name for converted version
    convFileName = deckboxDir
    convFileName = convFileName[:-4] + " converted.csv"

#Load file in csv Library
deckboxRead = csv.reader(open(deckboxDir))
deckboxList = list(deckboxRead)

dbRows = len(deckboxList)
dbCols = 0
for array in deckboxList:
    if dbCols < len(array):
        print(array)
        dbCols = len(array)


print(dbRows)
print(dbCols)

#Loop through spreadsheet and make 2D Array
