import os
import sys
import csv
import time
import json
import requests

#Global Variables
nameDict = {}
editDict = {}
condDict = {}


def createCSV():
    print("Please enter the directory of the file you want to convert.")
    print("NOTE: PLEASE make sure to follow the readMe instructions!")
    deckboxDir = input("\t")

    #check to validate it's actually a csv file
    if not os.path.isfile(deckboxDir) or deckboxDir[-4:] != ".csv":
        print(deckboxDir[:-4])
        print("Sorry, that path isn't valid!")
        sys.exit()
    else:
        #Making a file name for converted version
        convDir = deckboxDir[:-4] + " converted " + time.strftime("%Y%m%d-%H%M%S") + ".csv"
        global convFile
        convFile = open(convDir, 'w+')

    #Load file in csv Library
    deckboxRead = csv.reader(open(deckboxDir))
    deckboxList = list(deckboxRead)

    #Look at Deckbox spreadsheet for LxW parameters
    dbRows = len(deckboxList)
    dbCols = 16
    #Invalid param check
    if len(deckboxList[0]) != dbCols:
        print("Sorry, the file provided doesn't have the correct amount of columns! There should be " + str(dbCols))

    #Run edgeDefine for the 3 libraries we need to check
    edgeDefine()

    #Load file in csv Library
    deckboxRead = csv.reader(open(deckboxDir))
    deckboxList = list(deckboxRead)
    tcgWriter = csv.writer(convFile)

    #Loop through spreadsheet and initialize 2D Array to put values on
    tcgList = [['Set Name', 'Product Name', 'Number', 'Rarity', 'Condition', 'Total Quantity']]
    for y in range(1, dbRows):
        currRow = []

        #Set Name
        cardEdit = edgeCheck(deckboxList[y][3], "Edition")
        currRow.append(cardEdit)

        #Product Name
        cardName = edgeCheck(deckboxList[y][2], "Name")
        currRow.append(cardName)

        #Number
        currRow.append(deckboxList[y][4])

        #Rarity
        currRow.append(deckboxList[y][15][0].upper())

        #Condition
        currRow.append(edgeCheck(deckboxList[y][5], "Condition"))

        #Add to Quantity
        currRow.append(deckboxList[y][0])

        tcgList.append(currRow)


    with open(convDir, mode='w') as convFile:
        convFile = csv.writer(convFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        for row in tcgList:
            convFile.writerow(row)

def edgeDefine():
#Then make dict out of file contents
    global nameDict
    global editDict
    global condDict

    with open("nameCases.txt") as file:
        lines = file.readlines()
        #Start the array at 2 to check if there is at least 2 lines
        for i in range(1, len(lines), 2):
            #Go back to not skip any items
            #Take away last character since it's a newline character
            nameDict[lines[i - 1][:-1]] = lines[i][:-1]
    with open("editionCases.txt") as file:
        lines = file.readlines()
        for i in range(1, len(lines), 2):
            editDict[lines[i - 1][:-1]] = lines[i][:-1]
    with open("conditionCases.txt") as file:
        lines = file.readlines()
        for i in range(1, len(lines), 2):
            condDict[lines[i - 1][:-1]] = lines[i][:-1]

def edgeCheck(dbName, checkType):
    #Make switch case to open file based on checkType
    returnString = dbName

    if(checkType=="Edition"):
        if dbName in editDict:
            returnString = editDict[dbName]
    elif(checkType=="Name"):
        if dbName in nameDict:
            returnString = nameDict[dbName]
    elif(checkType == "Condition"):
        if dbName in condDict:
            returnString = condDict[dbName]
    #if dbname is in dict, change dbname
    #else just return it
    return returnString

def main():
    edgeDefine()
    createCSV()

    #Make selenium window
    #Log into TCGPlayer
    #Navigate TCGPlayer after

main()
