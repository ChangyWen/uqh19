import requests
import json
import numpy as np
import csv

def get_data_request(url, requestData):
    '''make HTTP GET request'''
    dResp = requests.get(url, headers = {'X-api-key': access_token}, params = requestData);       

    
    if dResp.status_code != 200:
        print("Unable to get data. Code %s, Message: %s" % (dResp.status_code, dResp.text));
    else:
        print("Data access successful")
        jResp = json.loads(dResp.text);
        return jResp



ric = 'JPY=' 
start_date = '2016-11-01'
end_date = '2019-06-30'

RESOURCE_ENDPOINT = "https://dsa-stg-edp-api.fr-nonprod.aws.thomsonreuters.com/data/historical-pricing/beta1/views/summaries/" + ric
access_token = 'D2QOOto7mMWybrtUy5sa4EgnYl8ToGi16mdJA0zc'  # your personal key for Data Science Accelerator access to Pricing Data
requestData = {
    "interval": "P1D",
    "start": start_date,
    "end": end_date,
    "fields": 'BID,ASK' #BID,ASK,OPEN_PRC,HIGH_1,LOW_1,TRDPRC_1,NUM_MOVES,TRNOVR_UNS
};

jResp = get_data_request(RESOURCE_ENDPOINT, requestData)

if jResp is not None:
    data = jResp[0]['data']
    headers = jResp[0]['headers']  
    names = [headers[x]['name'] for x in range(len(headers))]

# print(data)
# print(headers)
# print(names)
data = data[::-1]
file = open("USDJPY.csv", 'w',newline='')
writer = csv.writer(file)
writer.writerow(names)
for i in data:	
	writer.writerow(i)
file.close()