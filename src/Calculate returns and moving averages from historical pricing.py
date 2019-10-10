#!/usr/bin/env python
# coding: utf-8

# ## Historical pricing data 
# 
# Query EDP to get end of day pricing data for a specific stock (AAPL)

# In[ ]:


#Global imports

import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import requests
import json
import numpy as np

# get_ipython().run_line_magic('matplotlib', 'inline')
plt.style.use('seaborn')

# In[ ]:

# Global functions - make HTTP GET reqeust
def get_data_request(url, requestData):
    dResp = requests.get(url, headers = {'X-api-key': access_token}, params = requestData);       

    
    if dResp.status_code != 200:
        print("Unable to get data. Code %s, Message: %s" % (dResp.status_code, dResp.text));
    else:
        print("Data access successful")
        jResp = json.loads(dResp.text);
        return jResp


# <b><h2>Price History</b></h2>
# <body>Call the end of day pricing API to retrieve daily data. Display the data in a simple chart and table</body>

# In[ ]:


ric = 'AAPL.O' # APPLE
start_date = '2016-11-01'
end_date = '2019-06-30'

RESOURCE_ENDPOINT = "https://dsa-stg-edp-api.fr-nonprod.aws.thomsonreuters.com/data/historical-pricing/beta1/views/summaries/" + ric
access_token = 'Cpfhvmwtk1164oQlUUCks4y2yFfTZP9o9FT6KftU'
requestData = {
    "interval": "P1D",
    "start": start_date,
    "end": end_date,
    "fields": 'TRDPRC_1' #BID,ASK,OPEN_PRC,HIGH_1,LOW_1,TRDPRC_1,NUM_MOVES,TRNOVR_UNS
};

jResp = get_data_request(RESOURCE_ENDPOINT, requestData)


if jResp is not None:
    data = jResp[0]['data']
    headers = jResp[0]['headers']
    names = [headers[x]['name'] for x in range(len(headers))]
    close_price = pd.DataFrame(data, columns=names )
    
close_price.columns = ['DATE', 'CLOSE']
close_price.set_index(pd.to_datetime(close_price.DATE), inplace=True) # set the index to be the DATE
close_price.sort_index(inplace=True)  # sort the dataframe by the newly created datetime index

close_price.head()


# ### Moving averages
# 
# Calculate two moving averages, one for 20 and one for 50 days.

# In[ ]:


SMA1 = 20
SMA2 = 50

close_price['SMA20'] = close_price['CLOSE'].rolling(SMA1).mean()
close_price['SMA50'] = close_price['CLOSE'].rolling(SMA2).mean()


# In[ ]:


print(close_price.tail())


# In[ ]:

close_price.plot(title= ric + ' Close Price & SMA crossover',figsize=(16, 7))


# Calculate 1 day and 1 month returns

# In[ ]:


close_price['1DReturns'] = close_price['CLOSE'].pct_change(1)
close_price['1MReturns'] = close_price['CLOSE'].pct_change(21)
print(close_price.tail())


# In[ ]:


close_price['1DReturns'].plot(figsize = (16,7), title = "1 day Returns")
plt.savefig('../data/image/close_price_1DReturns.png')
plt.show()
plt.clf()
# In[ ]:


close_price['1MReturns'].plot(figsize = (16,7), title = "1 month Returns")

# In[ ]:
plt.savefig('../data/image/close_price_1MReturns.png')
plt.show()
plt.clf()
plt.close()