import requests
import csv
import json
import time

cryptocurrListings = {}
cryptocurrListingsMetadata = {}
url1 = "https://api.coinmarketcap.com/v2/listings/"
try:
    response = requests.get(url1)
    data = response.json()
    cryptocurrListings = data["data"]
    cryptocurrListingsMetadata = data["metadata"]
except:
    print("Exception while getting all cryptocurrency listings")


def check_startId_valid(startId):
    idInValid = True
    print("Inside the function: " + str(startId))
    tmp_dict = {}

    while(idInValid):
        try:
            url3 = url2 + str(startId) + "/"
            response = requests.get(url3)
            data = response.json()
            print("Inside try statement:")
            tmp_dict.update(data["data"])
            idInValid = False
        except:
            print("Exception: Id " + str(startId))
            idInValid = True
            startId += 1
    print("End of function " + str(startId))
    return startId
            
# Pull current data for all cryptocurrencies using the 'id' field
# Make a get request to get the cryptocurrency ticker data in order of rank using the 'ticker' endpoint.
url2 = "https://api.coinmarketcap.com/v2/ticker/"

start = 1
maxCalls = 30
cryptocurrdata = {}

for i in range(1, 21):
    #As there is a limit of 30 calls per minute, pausing the code for sometime after every 30 calls
    if(i % maxCalls == 0):
        print("Going to sleep for 60 seconds after 30 calls")
        time.sleep(60)
    
    start = check_startId_valid(start)

    parameters = {"start": start} 
    try:
        response = requests.get(url2, params=parameters)
        data = response.json()
        cryptocurrdata.update(data["data"])
    except:
        print("Exception in main for loop: Id " + str(start))
        
    start += 100

outfile = open("cryptocurrencydata.csv", "a+")
csvwriter = csv.writer(outfile)

count = 0
flattened_item = {}
for row in cryptocurrdata:
    item = cryptocurrdata[row]
    ######Start of code to flatten the response json#################################################################
    #Api response gives 'quotes' as a dict object. It is the price information in a particular
    #currency. Request parameters can specify quotes to be given in more than one currency. In this case, 'quotes' is a dict object with multiple
    #dicts inside it one for each currency. In order to write this to a csv file, the nested dict objects are flattened and keys are renamed to
    #indicate which currency they belong to.

    #Getting each currency in quotes as a list
    quote_keys = list(item["quotes"])
    quotes_dict = {}
    #Iterating over each currency using the list
    for elem in quote_keys:
        quotes_dict = item["quotes"][elem]
        newkey = ""
        orig_keys = list(quotes_dict)
        for k in orig_keys:
            newkey = "quotes" + "_" + elem + "_" + k
            quotes_dict[newkey] = quotes_dict.pop(k)
        
        flattened_item.update(quotes_dict)

    del item["quotes"]
    flattened_item.update(item)
    ######End of code to flatten the response json#################################################################
      
    #Using 'count' to write the keys as header row in csv file 
    if count == 0:
        header = flattened_item.keys()
        csvwriter.writerow(header)
        count += 1
    
    csvwriter.writerow(flattened_item.values())
 
outfile.close()

