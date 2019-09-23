#####################################
# ICON NODE MONITOR V2 BY RHIZOME #
#####################################

import datetime
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
	  text="*ALERT: " + dt.strftime("%Y-%m-%d %H:%M:%S") + "*" "\n" + "RHIZOME node is operational."
	)

def slack_alert_bad():
	slack_token = os.environ["SLACK_API_TOKEN"]
	client = slack.WebClient(token=slack_token)
	client.chat_postMessage(
	  channel="infrastructure-alerts",
	  text="*ALERT: " + dt.strftime("%Y-%m-%d %H:%M:%S") + "*" "\n" + "RHIZOME node `" + node_ip_pattern_match + "` is stuck at block height " + block_height_pattern_match1 + "."
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
response1 = requests.get(api_endpoint)
#Wait 2 seconds.
time.sleep(2)
#Make second response to API endpoint.
response2 = requests.get(api_endpoint)

#Store node IP as a variable.
node_ip_pattern = re.compile(r'\:\/\/(.*)\:9000')
for node_ip_pattern_match in re.findall(node_ip_pattern, api_input):
	pass
    #print(node_ip_pattern_match)

#If node returns a 503 response, print message and exit.
if response1.status_code == 503 or response2.status_code == 503:
	print("Node is returning a 503 response.")
	exit()

#Decode data from response.
data1 = response1.content.decode()
data2 = response2.content.decode()

#Define regex pattern to capture block height.
block_height_pattern = re.compile(r'\"block_height\"\:([0-9]*)\,\"')

#Extract block height number from data1 and data2.
for block_height_pattern_match1 in re.findall(block_height_pattern, data1):
	pass
for block_height_pattern_match2 in re.findall(block_height_pattern, data2):
	pass

#If the block height of request 1 and 2 are equal, let the user know blocks aren't being produced.
if block_height_pattern_match1 == block_height_pattern_match2:
	#print("Uh oh. New blocks are not being produced.")
	slack_alert_bad()
#If the block height of request 1 is less than 2, let the user know blocks are being produced.
elif block_height_pattern_match1 < block_height_pattern_match2:
	pass
	#print("Yay! New blocks are being produced.")
	slack_alert_good()
#If any other condition is satisfied, something is very wrong.
else:
	print("REKT.")

exit()