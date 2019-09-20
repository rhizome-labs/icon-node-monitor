import re
import requests
import time

#Ask for API endpoint.
api_input = input("What is your API endpoint? (e.g. http://104.196.209.29:9000) ")
api_endpoint = api_input + "/api/v1/avail/peer"
#print(api_endpoint)

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
pattern = re.compile(r'\"block_height\"\:([0-9]*)\,\"')

#Extract block height and print block_height number.
for match1 in re.findall(pattern, data1):
    print(match1)

#Wait 3 seconds before making the next API request.
time.sleep(3)

#Create second request to ping node.
response2 = requests.get(api_endpoint)

#If node returns a 503 response, alert the user and exit.
if response2.status_code == 503:
	print("Your node is reporting a 503 error.")
	quit()
#If node returns a 200 response, decode response and continue.
elif response2.status_code == 200:
	data1 = response1.content.decode()

#Extract block height and print block_height number.
for match2 in re.findall(pattern, data2):
    print(match2)

#If the block height of request 1 and 2 are equal, let the user know blocks aren't being produced.
if match1 == match2:
	print("Uh oh. New blocks are not being produced.")
#If the block height of request 1 is less than 2, let the user know blocks are being produced.
elif match1 < match2:
	print("Yay! New blocks are being produced.")
#If any other condition is satisfied, something is very wrong.
else:
	print("Something is very, very wrong.")

exit()