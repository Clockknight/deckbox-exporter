import os
import re
import sys
import csv
import time
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException

# Global Variables
nameDict = {}
editDict = {}
condDict = {}
rareDict = {}
delay = 4
scriptTime = time.strftime("%Y%m%d-%H%M%S")

with open("info.txt") as file:
    lines = file.readlines()
    username = lines[0]
    password = lines[1]


def managecardlisting(browser, argArray):
    listingMatch = False
    conditionString = argArray[4] + argArray[6]

    # Function for card management page, takes array of values (tcgRow) to ADD number of cards to inventory
    # browser should currently be at the card listing management url
    # listing table is the product table
    listingTable = wait.until(ec.element_to_be_clickable((By.ID, "ProductsTable"))).get_attribute('innerHTML')
    # find tds inside tbody
    listingSoup = BeautifulSoup(listingTable, "html.parser")
    # figure out rows
    listingRows = listingSoup.find("tbody").find_all("tr")

    # while loop to stop once match is found
    while not listingMatch:
        for listingIndex in range(0, len(listingRows)-1):
            listingRow = listingRows[listingIndex]
            # create array to manage info
            listingRowArray = []
            for listingItem in listingRow:
                listingRowArray.append(listingItem.get_text().strip())

            # compare condition row to argArray[4]
            # if it's a match
            if listingRowArray[1] == conditionString:
                # take textbox of that row input
                # xpath that leads to the table row with matching condition
                listingXpath = '//table/tbody/tr[' + str(listingIndex+1) + ']'
                # textbox should be in 6th td object
                listingTextbox = browser.find_element(By.XPATH, listingXpath + '/td[6]/div/input')

                # write the number of cards we're looking for (argArray[5])
                # NOTE: this overwrites any number, does NOT add numbers
                listingTextbox.clear()
                listingTextbox.send_keys(argArray[5])
                # look across tds to find one that doesn't have "-" as text
                # check if there's a pre-existing price from argArrays
                # then check slot 7 of the array
                listingPrice = 0.00
                if listingRowArray[7] != "-":
                    listingPrice = float(re.search(r"^\$\d{1,}\.\d{2}", listingRowArray[7]).group(0)[1:])
                # then check slot 5 of the array
                elif listingRowArray[5] != "-":
                    listingPrice = float(re.search(r"^\$\d{1,}\.\d{2}", listingRowArray[5]).group(0)[1:])
                # then check slot 3 of the array
                elif listingRowArray[3] != "-":
                    listingPrice = float(re.search(r"^\$\d{1,}\.\d{2}", listingRowArray[3]).group(0)[1:])
                # if all 3 dont exist
                else:
                    listingPrice = -100.00

                print(listingPrice)

                # then run fail case that returns to catalog page
                if listingPrice == -100:
                    argArray.append("No Listing Price Available")
                    failedRows.append(argArray)
                    browser.get("https://store.tcgplayer.com/admin/product/catalog")
                else:
                    listingTextbox = browser.find_element(By.XPATH, listingXpath + '/td[5]/div/input')
                    listingTextbox.clear()
                    listingTextbox.send_keys(str(listingPrice))

                # click the save button
                #listingButton = browser.find_element(By.XPATH, "/div[@id=inv-actions-wrapper-top]/inventory-actions/div/input[3]")
                browser.find_element(By.XPATH, "//div[@id='inv-actions-wrapper-top']/inventory-actions/div/input[3]").click()
                listingMatch = True

        if not listingMatch:
            argArray.append("No Direct Match Found")
            failedRows.append(argArray)
            browser.get("https://store.tcgplayer.com/admin/product/catalog")
            listingMatch = True


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
    elif checkType == "Rarity":
        if dbName in rareDict:
            returnString = rareDict[dbName]
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
try:
    wait.until(ec.element_to_be_clickable((By.ID, "logonButton"))).click()
except TimeoutException as ex:
    print("Script logged in by itself")

# Setup code before looking for cards
if not os.path.isfile(deckboxDir) or deckboxDir[-4:] != ".csv":
    print(deckboxDir[:-4])
    print("Sorry, that path isn't valid!")
    sys.exit()
else:
    # Making a file name for converted version
    convDir = deckboxDir[:-4] + " converted " + scriptTime + ".csv"

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
with open("rarityCases.txt") as file:
    lines = file.readlines()
    for i in range(1, len(lines), 2):
        rareDict[lines[i - 1][:-1]] = lines[i][:-1]

# Load file in csv Library
deckboxRead = csv.reader(open(deckboxDir))
deckboxList = list(deckboxRead)

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
    currRow.append(edgecheck(deckboxList[y][15], "Rarity"))
    # add foil if part #7 is equal to foil

    # Condition
    currRow.append(edgecheck(deckboxList[y][5], "Condition"))

    # Add to Quantity
    currRow.append(deckboxList[y][0])

    # Foil
    currRow.append(deckboxList[y][7])

    tcgList.append(currRow)

# write converted file, using tcgList
with open(convDir, mode='w') as convFile:
    convFile = csv.writer(convFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for row in tcgList:
        convFile.writerow(row)

# Use tcgList and for loop to search through using already converted data
# this loops once for each row/listing in the array
# Order of variables
# Set Name
# Product Name
# Number
# Rarity
# Condition (+ foil)
# Add to Quantity

# initialize failedRows, keeping TCG Header
failedRows = tcgList[0]

for tcgRow in tcgList[1:]:
    # Navigate TCGPlayer after logging in
    # Hard coded to choose option 1 (which is MTG)
    time.sleep(delay / 2)
    Select(wait.until(ec.element_to_be_clickable((By.ID, "CategoryId")))).select_by_value("1")
    # Choose Set name from csv
    time.sleep(delay/2)
    SetNameDropdown = browser.find_element(By.ID, 'SetNameId')
    textbox = browser.find_element(By.ID, "SearchValue")
    button = browser.find_element(By.ID, "Search")
    # reset variables
    matchBoolean = False

    # clear textbox to avoid accidental matches
    time.sleep(delay / 2)
    textbox.clear()

    # navigate search function using tcgRow values
    try:
        Select(SetNameDropdown).select_by_visible_text(tcgRow[0])
    except NoSuchElementException as e:
        # write to new cell in tcgRow since we wont be reading from it after this
        tcgRow.append("Condition Mismatch")
        # append row to failed rows
        failedRows.append(tcgRow)
        # move on to next item
        continue
    # wait inbetween inputs to let page process
    time.sleep(delay/2)
    # select by rarity
    Select(browser.find_element(By.ID, "Rarity")).select_by_visible_text(tcgRow[3])
    time.sleep(delay/2)
    # search card name
    textbox.send_keys(str(tcgRow[1]))
    # let the website search
    button.click()
    time.sleep(delay/2)

    # If the current url is still catalog page
    # usually caused by multiple matches
    if browser.current_url == "https://store.tcgplayer.com/admin/product/catalog":
        # Find table
        table = browser.find_element(By.ID, "ProductsTable").get_attribute('innerHTML')
        # find tds inside tbody
        soup = BeautifulSoup(table, "html.parser")
        tableRows = soup.find("tbody").find_all("tr")
        # for each td
        for row in tableRows:
            # create array for the row based on each td
            rowArray = []
            for item in row.find_all("td"):
                rowArray.append(item.get_text().strip())

            # compare name to make sure name is not a partial match
            if rowArray[1] == tcgRow[1]:
                # compare against number
                if rowArray[4] == "Card # " + tcgRow[2]:
                    # if both values match parameters run managecardlisting and break for loop
                    managecardlisting(browser, tcgRow)
                    matchBoolean = True
                    break

        # If there's no more tds, and no match was found
        if not matchBoolean:
            # Put row in a new array for writing errors
            tcgRow.append("No Match Found")
            failedRows.append(tcgRow)
        # At the end of the program, write the array to a failed csv

    # else, run managecardlisting
    else:
        managecardlisting(browser, tcgRow)

# write failed rows to csv
convDir = deckboxDir[:-4] + " failed " + scriptTime + ".csv"
with open(convDir, mode='w') as convFile:
    convFile = csv.writer(convFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    for row in tcgList:
        convFile.writerow(failedRows)