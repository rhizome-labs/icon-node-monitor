#####################################
# ICON NODE MONITOR V0.1 BY RHIZOME #
#####################################

import datetime
import os
import re
import requests
import slack
import time

#Declare current date and time.
dt = datetime.datetime.now()

def slack_alert_good():
	slack_token = os.environ["SLACK_API_TOKEN"]
	client = slack.WebClient(token=slack_token)
	client.chat_postMessage(
	  channel="infrastructure-alerts",
	  text="*ALERT: " + dt.strftime("%Y-%m-%d %H:%M:%S") + "*" "\n" + "RHIZOME node `" + node_ip_pattern_match + "` is stuck at block height " + block_height_pattern_match1 + "."
	)

def slack_alert_bad():
	slack_token = os.environ["SLACK_API_TOKEN"]
	client = slack.WebClient(token=slack_token)
	client.chat_postMessage(
	  channel="infrastructure-alerts",
	  text="*ALERT: " + dt.strftime("%Y-%m-%d %H:%M:%S") + "*" "\n" + "RHIZOME node `" + node_ip_pattern_match + "` is stuck at block height " + block_height_pattern_match1 + "."
	)

#Ask for API endpoint.
#api_input = input("What is your API endpoint? (e.g. http://104.196.209.29:9000) ")
api_input = "http://104.196.209.29:9000"
api_endpoint = api_input + "/api/v1/avail/peer"
#print(api_endpoint)

#Store node IP as a variable.
node_ip_pattern = re.compile(r'\:\/\/(.*)\:9000')
for node_ip_pattern_match in re.findall(node_ip_pattern, api_input):
	pass
    #print(node_ip_pattern_match)

#Create first request to ping node.
response1 = requests.get(api_endpoint)

#If node returns a 503 response, alert the user and exit.
if response1.status_code == 503:
	print("Your node is reporting a 503 error.")
	quit()
#If node returns a 200 response, decode response and continue.
elif response1.status_code == 200:
	data1 = response1.content.decode()

#Define regex match pattern for block height.
block_height_pattern = re.compile(r'\"block_height\"\:([0-9]*)\,\"')

#Extract block height and print block_height number.
for block_height_pattern_match1 in re.findall(block_height_pattern, data1):
	pass
    #print(block_height_pattern_match1)

#Wait before making the next API request.
time.sleep(2)

#Create second request to ping node.
response2 = requests.get(api_endpoint)

#If node returns a 503 response, alert the user and exit.
if response2.status_code == 503:
	print("Your node is reporting a 503 error.")
	quit()
#If node returns a 200 response, decode response and continue.
elif response2.status_code == 200:
	data2 = response2.content.decode()

#Extract block height and print block_height number.
for block_height_pattern_match2 in re.findall(block_height_pattern, data2):
	pass
    #print(block_height_pattern_match2)

#If the block height of request 1 and 2 are equal, let the user know blocks aren't being produced.
if block_height_pattern_match1 == block_height_pattern_match2:
	#print("Uh oh. New blocks are not being produced.")
	slack_alert_good()
#If the block height of request 1 is less than 2, let the user know blocks are being produced.
elif block_height_pattern_match1 < block_height_pattern_match2:
	#print("Yay! New blocks are being produced.")
	slack_alert_bad()
#If any other condition is satisfied, something is very wrong.
else:
	print("REKT.")

exit()