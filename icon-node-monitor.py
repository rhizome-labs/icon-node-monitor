#####################################
# ICON NODE MONITOR V2 BY RHIZOME #
#####################################

import datetime
import json
import os
import re
import requests
import slack
import time

#Declare current date and time.
dt = datetime.datetime.now()

#Create Slack message.
def slack_alert_good():
	slack_token = os.environ["SLACK_API_TOKEN"]
	client = slack.WebClient(token=slack_token)
	client.chat_postMessage(
	  channel="infrastructure-alerts",
	  text="*ALERT: " + dt.strftime("%Y-%m-%d %H:%M:%S") + "*" "\n" + "Node " + node_ip + " is operational."
	)

def slack_alert_bad():
	slack_token = os.environ["SLACK_API_TOKEN"]
	client = slack.WebClient(token=slack_token)
	client.chat_postMessage(
	  channel="infrastructure-alerts",
	  text="*ALERT: " + dt.strftime("%Y-%m-%d %H:%M:%S") + "*" "\n" + "Node " + "`" + api_input + "`" " is stuck at block height " + str(block_height1) + "." + "\n" + "Please check the following server(s): " + node_ip + "."
	)

#Pass API endpoint from environment variable.
api_input = os.environ["API_ENDPOINT"]

#Add "http://" or "https://" if not specified in the environment variable.
if "http://" in api_input or "https://" in api_input:
	api_endpoint = api_input + "/api/v1/avail/peer"
else:
	api_endpoint = "http://" + api_input + "/api/v1/avail/peer"

#print(api_endpoint)

#Make first response to API endpoint.
response1 = requests.get(api_endpoint, timeout=30)
#Wait 2 seconds.
time.sleep(2)
#Make second response to API endpoint.
response2 = requests.get(api_endpoint, timeout=30)

#Encode response1 and response2 JSON, and extract block height.
block_height1 = json.loads(response1.content.decode())['block_height']
block_height2 = json.loads(response2.content.decode())['block_height']
#print(block_height1)
#print(block_height2)

#Store node IP for response1 and response2 as variables.
node_ip1 = json.loads(response1.content.decode())['peer_target'].rstrip(':7100')
node_ip2 = json.loads(response2.content.decode())['peer_target'].rstrip(':7100')
#Set value for node_ip depending on if the IPs for the two requests are the same.
if node_ip1 == node_ip2:
	node_ip = "`" + node_ip1 + "`"
else:
	node_ip = "`" + node_ip1 + "`"+ " and " + "`" + node_ip2 + "`"

#If the block height of request 1 and 2 are equal, let the user know blocks aren't being produced.
if block_height1 == block_height2:
	#print("Uh oh. New blocks are not being produced.")
	slack_alert_bad()
#If the block height of request 1 is less than 2, let the user know blocks are being produced.
else:
	#print("Yay! New blocks are being produced.")
	#slack_alert_good()
	pass

exit()