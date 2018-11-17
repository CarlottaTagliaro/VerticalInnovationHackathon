"""Python server consuming LoRaServer and InfluxDB APIs

Copyright (C) 2018  Eurac Research - Center for Sensing Solutions
This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software Foundation,
Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301  USA"""

import requests
import warnings
import time
import json

# Global variables
loraAPI_url = "http://saocompute.eurac.edu/LoRaApp/api/"
influxAPI_url = "http://saocompute.eurac.edu/sensordb/query"
database = "loraton_texel" # the database name here
username = "texel" # your username here
password = "dBNLyn3BL3vbcE2B" # your password here
dev_EUI = "0099f60988d034e8" # your device EUI here
TIME_SLEEP = 5
server_ip = "127.0.0.1"
server_port = "8000"

# JWT generation method needed to query the LoRa App Server API
def regenerateJWT(password,username):
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    url = loraAPI_url + 'internal/login'
    data = {"password": password, "username": username}
    response = postRequest(url, headers, data)
    print(response.content)
    if (response.status_code == 200):
        new_jwt = json.loads(response.content.decode())['jwt']
        return new_jwt
    else:
        print("Problems in generating a new JWT")
        return -1

# Downlink building method
def sendDownlink(jwt, message):
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Grpc-Metadata-Authorization': 'Bearer ' + jwt
    }

    url = loraAPI_url + 'devices/' + dev_EUI + '/queue'
    print(url)
    data = {"deviceQueueItem": {"confirmed": True, "devEUI": dev_EUI,
                                "fCnt": getFrameUplink(jwt), "fPort": 2, "jsonObject": message}}
    response = postRequest(url, headers, data)
    if (response.status_code == 200):
        print("Message sent")
    else:
        print(response.content)
        print("Problems in sending message")

# Uplink-Downlink synchronization method
def getFrameUplink(jwt):
    headers = {
        'Accept': 'application/json',
        'Grpc-Metadata-Authorization': 'Bearer ' + jwt
    }

    url = loraAPI_url + 'devices/' + dev_EUI + '/activation'
    response = getRequest(url, headers)
    frameuplink = json.loads(response.content.decode())['deviceActivation']['fCntUp']

    if (response.status_code == 200):
        #print("Frame uplink retrieved successfully")
        return frameuplink
    else:
        print("Problem in retrieving the frame uplink.")
        return 0

# GET request method
def getRequest(url, headers):
    return requests.get(url, verify=False, headers=headers)


# POST request method
def postRequest(url, headers, data):
    return requests.post(url, verify=False, headers=headers, json=data)

# Main body
warnings.filterwarnings("ignore")
current_jwt = regenerateJWT(password,username)
database = "?db="+database
username = "&u="+username
password = "&p="+password
first_loop = True
old_value = ""

if(current_jwt!=-1):

    while (True):

        warnings.filterwarnings("ignore")

        # Query that retrieves the last value stored into the InfluxDB database
        base_url = influxAPI_url + database + username + password
        query_url = "SELECT device_name, value FROM device_frmpayload_data_message WHERE dev_eui='" + dev_EUI + "' ORDER BY time DESC LIMIT 1"
        final_url = base_url + "&q=" + query_url
        response = requests.get(final_url)
        jsonresult = json.loads(response.content.decode())['results'][0]['series'][0]
        print("DEV_NAME " + jsonresult['values'][0][1])
        value = jsonresult['values'][0][2]
        print("VALUE_STORED " + value)

        if(first_loop):
            old_value = value
            first_loop = False
        if(value != old_value):
            if value.find("code=") != -1:
                try:
                    correct = bool(int(requests.get("http://" + server_ip + ":" + server_port + "/bivacchi/checkcode/1/?code=" +value.split("code=")[1]).content.decode()))
                except:
                    correct = False
                if correct:
                    downlink_msg = str('{"message":"correct"}')
                else:
                    downlink_msg = str('{"message":"incorrect"}')
            elif value.find("temp=") != -1:
                try:
                    requests.get("http://" + server_ip + ":" + server_port + "/bivacchi/temperature/1/?temp=" +value.split("temp=")[1]).content.decode()
                except:
                    print("Error sending temp")
            elif bool(int(requests.get("http://" + server_ip + ":" + server_port + "/bivacchi/bar/1/").content.decode())):
                downlink_msg = str('{"message":"open"}')
            else:
                downlink_msg = str('{"message":"close"}')
            print(downlink_msg)
            sendDownlink(current_jwt, downlink_msg)
            old_value = value
        else:
            print("Same value")

        print("----------------------------------------------------------")

        time.sleep(TIME_SLEEP)
else:
    print("Some problem occurred... exiting the script")