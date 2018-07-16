# CoinmarketData
This is a simple program to use CoinMarketData APIs to get current ticker data for all listed cryptocurrencies and do some basic analysis. 

A Python script is written to obtain data using the CoinMarketData APIs. This data is saved as a CSV file locally in the script itself. This CSV file is uploaded to Google Cloud Storage bucket. A dataset and table is created in Google BigQuery using this CSV file. A Cloud Datalab Instance is created and some sql analysis is done in a notebook using the BigQuery table.
