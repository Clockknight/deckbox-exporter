import os
import sys
import csv
import time
import json
import requests

#Global variables
nameDict = {}
editDict = {}
condDict = {}

#Global API variables
with open("./info.txt") as file:
    lines = file.readlines()

session = requests.session()

api = "bearer " + lines[7][:-1]
keys = {
    "Authorization":api,
    "Content-Type":"application/json"
}
url = "https://api.tcgplayer.com/v1.39.0/catalog/categories/1/search"
page = session.get(url)
session.headers.update(keys)

def updateBody(name, set):
    body = {
        "limit":10000,
        "filters":[ {
                        "name": "ProductName",
                        "values": [name]
                    },
                    {
                        "name": "Set Name",
                        "values": [set]

                    }, ]
    }
    return body

def main():
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
    tcgList = [['TCGplayer Id', 'Product Line', 'Set Name', 'Product Name', 'Title', 'Number', 'Rarity', 'Condition', 'TCG Market Price', 'TCG Direct Low', 'TCG Low Price With Shipping', 'TCG Low Price', 'Total Quantity', 'Add to Quantity', 'TCG Marketplace Price', 'Photo URL']]
    for y in range(1, dbRows):
        currRow = []
        filler = "1" #Filler text to put in columns that don't care about what value is input
        #TCGplayer ID
        #We'll get the actual ID later. Leaving this column to fill after all the info is gotten.
        currRow.append("TODO")

        #Product Line
        currRow.append("Magic")

        #Set Name
        cardEdit = edgeCheck(deckboxList[y][3], "Edition")
        currRow.append(cardEdit)

        #Product Name
        cardName = edgeCheck(deckboxList[y][2], "Name")
        currRow.append(cardName)

        #Title
        currRow.append(filler)

        #Number
        currRow.append(deckboxList[y][4])

        #Rarity
        currRow.append(deckboxList[y][15][0].upper())

        #Condition
        cardCond = edgeCheck(deckboxList[y][5], "Condition")
        currRow.append(cardCond)

        #TCG Market Price
        currRow.append(filler)

        #TCG Direct Low
        currRow.append(filler)

        #TCG Low Price With Shipping
        currRow.append(filler)

        #TCG Low Price
        currRow.append(filler)

        #Total Quantity
        currRow.append(filler)

        #Add to Quantity
        currRow.append(deckboxList[y][0])

        #TCG Marketplace Price
        currRow.append(filler)

        #Photo URL
        currRow.append(filler)

        #Actually get TCG ID
        body = updateBody(cardName, cardEdit)
        print(str(y) + " / " + str(dbRows-1), end = "\t")
        bodyResponse = json.loads(session.post(url, json=body).text)["results"]
        if(len(bodyResponse) == 1):
            print("")
            currRow[0] = bodyResponse[0]
        elif(len(bodyResponse) > 1):
            print(" Multiple Response Error")
            currRow[0] = ""
        else:
            print(" No Response Error")
            currRow[0] = ""

        tcgList.append(currRow)


    with open(convDir, mode='w') as convFile:
        convFile = csv.writer(convFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        for row in tcgList:
            convFile.writerow(row)

def edgeDefine():
#Then make dict out of file contents
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
    returnName = dbName

    if(checkType=="Edition"):
        if dbName in editDict:
            returnName = editDict[dbName]
    elif(checkType=="Name"):
        if dbName in nameDict:
            returnName = nameDict[dbName]
    elif(checkType == "Condition"):
        if dbName in condDict:
            returnName = condDict[dbName]
    #if dbname is in dict, change dbname
    #else just return it
    return returnName

main()
