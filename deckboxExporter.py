import os
import sys
import csv
import time

def main():
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
        convDir = deckboxDir[:-4] + " converted " + time.strftime("%Y%m%d-%H%M%S") + ".csv"
        convFile = open(convDir, 'w+')

    #Load file in csv Library
    deckboxRead = csv.reader(open(deckboxDir))
    deckboxList = list(deckboxRead)
    tcgWriter = csv.writer(convFile)

    dbRows = len(deckboxList)
    dbCols = 16
    if len(deckboxList[0]) != dbCols:
        print("Sorry, the file provided doesn't have the correct amount of columns! There should be " + str(dbCols))

    #Loop through spreadsheet and initialize 2D Array to put values on
    tcgList = [['TCGplayer Id', 'Product Line', 'Set Name', 'Product Name', 'Title', 'Number', 'Rarity', 'Condition', 'TCG Market Price', 'TCG Direct Low', 'TCG Low Price With Shipping', 'TCG Low Price', 'Total Quantity', 'Add to Quantity', 'TCG Marketplace Price', 'Photo URL']]
    for y in range(1, dbRows):
        currRow = []
        variable = ""
        filler = "---"
        #TCGplayer ID
        currRow.append("TODO")

        #Product Line
        currRow.append("Magic")

        #Set Name
        currRow.append(deckboxList[y][3])

        #Product Name
        currRow.append(deckboxList[y][2])

        #Title
        currRow.append(filler)

        #Number
        currRow.append(deckboxList[y][4])

        #Rarity
        currRow.append(deckboxList[y][15][0].upper())

        #Condition
        variable = deckboxList[y][5]
        #switchcase to catch condition
        currRow.append(variable)

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

        tcgList.append(currRow)


    with open(convDir, mode='w') as convFile:
        convFile = csv.writer(convFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        for row in tcgList:
            print(row[0])
            convFile.writerow(row)
'''
#DELETE
#Ugly print check
    for thing in deckboxList:
        print(thing)
    for thing in tcgList:
        print("\nitem")
        for i in range(0, len(tcgList[0])):
            print(tcgList[0][i] + ": " + thing[i])
'''

def edgeCheck(dbName, checkType):
    #Make switch case to open file based on checkType
    #Then make dict out of file contents
    edgeDict = {}
    switch(checkType)
    {
        case("Set Name"):
        break;
        case("Product Name"):
        break;
        case("Condition"):
        break;
    }
    #if dbname is in dict, change dbname
    #else just return it

    return dbName

main()
