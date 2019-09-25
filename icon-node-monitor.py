###################################
# ICON NODE MONITOR V2 BY RHIZOME #
###################################

import datetime
import json
import os
import re
import requests
import slack
import telegram
import time

#Declare current date and time.
dt = datetime.datetime.now()

#Create Slack alert messages.
def slack_alert_good():
	slack_api_token = os.environ["SLACK_API_TOKEN"]
	slack_bot = slack.WebClient(token=slack_api_token)
	slack_bot.chat_postMessage(channel="infrastructure-alerts", text=alert_good)

def slack_alert_bad():
	slack_api_token = os.environ["SLACK_API_TOKEN"]
	slack_bot = slack.WebClient(token=slack_api_token)
	slack_bot.chat_postMessage(channel="infrastructure-alerts", text=alert_bad)

#Create Telegram alert messages.
def tg_alert_good():
	tg_bot_token = os.environ["TG_BOT_TOKEN"]
	tg_chat_id = os.environ["TG_CHAT_ID"]
	tg_bot = telegram.Bot(token=tg_bot_token)
	tg_bot.send_message(chat_id=tg_chat_id, text=alert_good, parse_mode=telegram.ParseMode.MARKDOWN)

def tg_alert_bad():
	tg_bot_token = os.environ["TG_BOT_TOKEN"]
	tg_chat_id = os.environ["TG_CHAT_ID"]
	tg_bot = telegram.Bot(token=tg_bot_token)
	bot.send_message(chat_id=tg_chat_id, text=alert_bad, parse_mode=telegram.ParseMode.MARKDOWN)

#Exit if no API endpoint is provided.
if os.environ["API_ENDPOINT"] == "":
		time.sleep(1)
		print("ERROR! Please specify your API endpoint as an environment variable (e.g. API_ENDPOINT=\"https://ctz.rhizomeicx.com\").")
		time.sleep(1)
		print("Exiting now...")
		time.sleep(2)
		exit()

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

#Declare alert messages.
alert_good = "*ALERT: " + dt.strftime("%Y-%m-%d %H:%M:%S") + "*" "\n" + "Node " + node_ip + " is operational."
alert_bad = "*ALERT: " + dt.strftime("%Y-%m-%d %H:%M:%S") + "*" "\n" + "Node " + api_input + " is stuck at block height " + str(block_height1) + "." + "\n" + "Please check the following server(s): " + node_ip + "."
#Remove markdown formatting for Terminal alerts.
alert_good_raw = re.sub('[`*]', '', alert_good)
alert_bad_raw = re.sub('[`*]', '', alert_bad)

#If the block height of request 1 and 2 are equal, let the user know blocks aren't being produced.
if block_height1 == block_height2:
	#Print alert in Terminal.
	print(alert_bad_raw)
	#Send Slack alert if Slack API token is specified.
	if os.environ["SLACK_API_TOKEN"] == "":
		print("Slack token is not configured.")
	else:
		slack_alert_bad()
	#Send Telegram alert if Telegram API token is specified.
	if os.environ["TG_BOT_TOKEN"] == "" or os.environ["TG_CHAT_ID"] == "":
		print("Telegram token is not configured.")
	else:
		tg_alert_bad()
		
#If the block height of request 1 is less than 2, let the user know blocks are being produced.
else:
	#Print alert in Terminal.
	print(alert_good_raw)
	#Send Slack alert if Slack API token is specified.
	if os.environ["SLACK_API_TOKEN"] == "":
		print("Slack token is not configured.")
	else:
		slack_alert_good()
	#Send Telegram alert if Telegram API token is specified.
	if os.environ["TG_BOT_TOKEN"] == "" or os.environ["TG_CHAT_ID"] == "":
		print("Telegram token is not configured.")
	else:
		tg_alert_good()
exit()