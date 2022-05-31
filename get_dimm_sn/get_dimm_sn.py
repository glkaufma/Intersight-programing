"""
    get_dimm_sn.py - The script was created to support Field Notice: FN - 72368 - Some DIMMs Might Fail Prematurely Due
    to a Manufacturing Deviation - Hardware Upgrade Available. https://www.cisco.com/c/en/us/support/docs/field-notices/723/fn72368.html

    This script makes API calls to obtian Serial Numbers for all DIMMs from servers being manageed by Intersight

    We will leverage "intersight_auth.py" from the DevNet learning labs to handle authentication, thanks Chris Gascoigne!

    author: Glen Kaufman (glkaufma@cisco.com)
"""
import os
import json
from numpy import save
import requests
import pandas as pd
import openpyxl
from intersight_auth import IntersightAuth

key_path = '/Users/glkaufma/Documents/Intersight-programing/'

# Create an AUTH object, you will need a secret and api key from the Intersight instance of interest.
AUTH = IntersightAuth(
    secret_key_filename = key_path + 'SecretKey.txt',
    api_key_id = '<paste API Key here>'
    )

# Intersight REST API Base URL
BURL = 'https://www.intersight.com/api/v1/'

#API path to the memory inventory JSON object
resource_path = 'memory/Units'

#API query parameters, these determine what properties we are collecting for each memory object.
query_parameters = '?$select=Serial,Dn,Location,RegisteredDevice&$expand=RegisteredDevice($select=DeviceHostname)&$top=1000'

''' Insights API calls are limited to 1000 response elements.  Since there more then 1000 memory elements we will need to step through every 1000
 and concantinate.
'''

#getting total number of memory elements
response=requests.get(BURL + resource_path +'?$count=true',auth=AUTH )
count = json.loads(response.text).get('Count')

#output the number of DIMM modules and requests needed
print('The number of DIMM modules are: ', count)
count = count//1000
print('The number of requests needed is :', count)

#creating an empty list and dictionary, these will be populated from the API calls
memory_list = []
memory_dict = {}

#making API calls for the data we need for each memory module in chunks of 1000, items of interest are determined by query_paramters
for i in range(count+1): 
   print('Grabbing 1000 memory module chunk ', i*1000, 'to', i*1000+1000)
   response = requests.get(BURL + resource_path + query_parameters + '&$skip=' + str(i*1000),auth=AUTH)
   memory_dict_append = json.loads(response.text)
   memory_list_append = memory_dict_append['Results']
   memory_list.append(memory_list_append)
   
#setting up an empty pandas dataframe
column_names=['Serial','Dn','Location','Hostname']
mem_df=pd.DataFrame([],columns=column_names)

#running through the list of dictionaries to add data to the empty dataframe skiping any empty (null) serial number
for i in range(count+1):
    for l in range(len(memory_list[i])):
        if memory_list[i][l]['Serial'] != '':
            new_row = {'Serial':memory_list[i][l]['Serial'], 'Dn':memory_list[i][l]['Dn'], 'Location':memory_list[i][l]['Location'], 'Hostname':memory_list[i][l]['RegisteredDevice']['DeviceHostname'][0]}
            new_row_df = pd.DataFrame(new_row,columns=column_names,index=[0])
            mem_df = pd.concat([mem_df,new_row_df], ignore_index=True)


save_path = '/Users/glkaufma/Documents/Intersight-programing/'
#creating a csv text file with the list of serial numbers, this will be uploaded using the SN checker tool
mem_df.to_csv(save_path + 'serial.txt',columns=['Serial'],index=False,header=False)

#creating an excel file with Serial, Dn, Location and Hostname so that we can identify any memory impacted
writer = pd.ExcelWriter(save_path + 'serial_all.xlsx')
mem_df.to_excel(writer, index=False, engine='openpyxl')
writer.save()  