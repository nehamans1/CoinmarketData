import requests
import csv
import json
import time

#Using Listings endpoint to fetch all listed cryptocurrencies
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

# Pull current data for each of the listed cryptocurrencies using the 'id' field
url2 = "https://api.coinmarketcap.com/v2/ticker/"

start = 1
maxCalls = 30
cryptocurrdata = {}

for eachId in cryptocurrListings:
    print("Iteration Number: " + str(start))
    print("Id: " + str(eachId["id"]))
    #As there is a limit of 30 calls per minute, pausing the code for sometime after every 30 calls using the 'start' counter
    if(start % maxCalls == 0):
        print("Going to sleep for 60 seconds after 30 calls")
        time.sleep(60)
    
    #parameters = {"start": eachIdls["id"], "limit":1} 
    try:
        response = requests.get(url2+str(eachId["id"])+"/")
        #response = requests.get("https://api.coinmarketcap.com/v2/ticker/101/")
        data = response.json()
        cryptocurrdata[eachId["id"]] = data["data"]
        with open('data.txt', 'w') as outfilejson:  
            json.dump(cryptocurrdata, outfilejson)
    except:
        print("Exception: Id " + str(eachId["id"]))
        
    start += 1

###########################################################################################################################
#####Once all data is fetched using the APIs, writing the json to a csv file###############################################
outfile = open("cryptocurrencydata.csv", "w")
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
        #For each currency, getting all the information i.e. all key/values in a dict
        quotes_dict = item["quotes"][elem]
        newkey = ""
        #Converting this dict to a list for modifying the key names at the same time as iterating over the dict. If not converted
        #to a list then iterating over the dict and modifying at the same time leads to errors in Python 3
        orig_keys = list(quotes_dict)
        #Iterating over each key and renaming it to 'quotes_<curr>_<key>'
        for k in orig_keys:
            newkey = "quotes" + "_" + elem + "_" + k
            quotes_dict[newkey] = quotes_dict.pop(k)
        
        #Creating a new dict and updating it with the renamed & flattened 'quotes'
        flattened_item.update(quotes_dict)

    #Removing the nested 'quotes' dict from the original dict
    del item["quotes"]
    #Adding the remaining keys from the original dict to the new flattened dict
    flattened_item.update(item)
    ######End of code to flatten the response json#################################################################
      
    #Using 'count' to write the keys as header row in csv file 
    if count == 0:
        header = flattened_item.keys()
        csvwriter.writerow(header)
        count += 1
    
    csvwriter.writerow(flattened_item.values())
 
outfile.close()
#####End of writing json to csv file###############################################
###########################################################################################################################
