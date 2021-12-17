import os
import sys
import csv
import time
import requests
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup

# Global Variables
nameDict = {}
editDict = {}
condDict = {}
delay = 4
with open("info.txt") as file:
    lines = file.readlines()
    username = lines[0]
    password = lines[1]


def managecardlisting(browser, argArray):
    # Function for card management page, takes array of values (tcgRow) to ADD number of cards to inventory
    print("managing card")

def edgecheck(dbName, checkType):
    # Make switch case to open file based on checkType
    returnString = dbName

    if checkType == "Edition":
        if dbName in editDict:
            returnString = editDict[dbName]
    elif checkType == "Name":
        if dbName in nameDict:
            returnString = nameDict[dbName]
    elif checkType == "Condition":
        if dbName in condDict:
            returnString = condDict[dbName]
    # if dbname is in dict, change dbname
    # else just return it
    return returnString


print("Please enter the directory of the file you want to convert.")
print("NOTE: PLEASE make sure to follow the readMe instructions!")
deckboxDir = input("\t")
# Make selenium window
s = Service(ChromeDriverManager().install())
browser = webdriver.Chrome(service=s)
browser.maximize_window()
browser.get("https://store.tcgplayer.com/admin/product/catalog")
wait = WebDriverWait(browser, delay)
# Log into TCGPlayer
wait.until(ec.element_to_be_clickable((By.ID, "UserName"))).send_keys(username)
wait.until(ec.element_to_be_clickable((By.ID, "Password"))).send_keys(password)
wait.until(ec.element_to_be_clickable((By.ID, "logonButton"))).click()
# Navigate TCGPlayer after logging in
# Hard coded to choose option 1 (which is MTG)
Select(wait.until(ec.element_to_be_clickable((By.ID, "CategoryId")))).select_by_value("1")

# Setup code before looking for cards
if not os.path.isfile(deckboxDir) or deckboxDir[-4:] != ".csv":
    print(deckboxDir[:-4])
    print("Sorry, that path isn't valid!")
    sys.exit()
else:
    # Making a file name for converted version
    convDir = deckboxDir[:-4] + " converted " + time.strftime("%Y%m%d-%H%M%S") + ".csv"
    global convFile
    convFile = open(convDir, 'w+')

# Load file in csv Library
deckboxRead = csv.reader(open(deckboxDir))
deckboxList = list(deckboxRead)

# Look at Deckbox spreadsheet for LxW parameters
dbRows = len(deckboxList)
dbCols = 16
# Invalid param check
if len(deckboxList[0]) != dbCols:
    print("Sorry, the file provided doesn't have the correct amount of columns! There should be " + str(dbCols))

# define global variables using text files to convert deckbox values into TCGPlayer OK versions
with open("nameCases.txt") as file:
    lines = file.readlines()
    # Start the array at 2 to check if there is at least 2 lines
    for i in range(1, len(lines), 2):
        # Go back to not skip any items
        # Take away last character since it's a newline character
        nameDict[lines[i - 1][:-1]] = lines[i][:-1]
with open("editionCases.txt") as file:
    lines = file.readlines()
    for i in range(1, len(lines), 2):
        editDict[lines[i - 1][:-1]] = lines[i][:-1]
with open("conditionCases.txt") as file:
    lines = file.readlines()
    for i in range(1, len(lines), 2):
        condDict[lines[i - 1][:-1]] = lines[i][:-1]

# Load file in csv Library
deckboxRead = csv.reader(open(deckboxDir))
deckboxList = list(deckboxRead)
tcgWriter = csv.writer(convFile)

# Loop through spreadsheet and initialize 2D Array to put values on
tcgList = [['Set Name', 'Product Name', 'Number', 'Rarity', 'Condition', 'Total Quantity']]
for y in range(1, dbRows):
    currRow = []

    # Set Name
    cardEdit = edgecheck(deckboxList[y][3], "Edition")
    currRow.append(cardEdit)

    # Product Name
    cardName = edgecheck(deckboxList[y][2], "Name")
    currRow.append(cardName)

    # Number
    currRow.append(deckboxList[y][4])

    # Rarity
    currRow.append(deckboxList[y][15])

    # Condition
    currRow.append(edgecheck(deckboxList[y][5], "Condition"))

    # Add to Quantity
    currRow.append(deckboxList[y][0])

    tcgList.append(currRow)

with open(convDir, mode='w') as convFile:
    convFile = csv.writer(convFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    for row in tcgList:
        convFile.writerow(row)

convReadFile = open(convDir, mode='r')

# Choose Set name from csv
time.sleep(delay/2)
SetNameDropdown = browser.find_element(By.ID, 'SetNameId')

#Define HTML elements like the textbox that dont change
textbox = browser.find_element(By.ID, "SearchValue")
button = browser.find_element(By.ID, "Search")

# Use tcgList and for loop to search through using already converted data

for tcgRow in tcgList[1:]:
    # Order of variables
        # Set Name
        # Product Name
        # Number
        # Rarity
        # Condition
        # Add to Quantity
    Select(SetNameDropdown).select_by_visible_text(tcgRow[0])
    time.sleep(delay/2)
    Select(browser.find_element(By.ID, "Rarity")).select_by_visible_text(tcgRow[3])
    time.sleep(delay/2)
    textbox.clear()
    textbox.send_keys(str(tcgRow[1]))
    button.click()
    time.sleep(delay/2)

    # If the current url is still https://store.tcgplayer.com/admin/product/catalog
    if browser.current_url == "https://store.tcgplayer.com/admin/product/catalog":
        # Find table
        listingTable = browser.find_element(By.CLASS_NAME, "display dTable")
        # find tds inside tbody
        soup = BeautifulSoup(listingTable)
        tableRows = soup.find("tbody").find_all("td")
        # for each td
        for row in tableRows:
            # compare name to make sure name is not a partial match
            # compare against number

            #
            # break if both values match parameters

        # If there's no more tds
            # Put row in a new array for writing errors
            # At the end of the program, write the array to a failed csv

    # else, run managecardlisting
    else:
        managecardlisting(browser, tcgRow)




