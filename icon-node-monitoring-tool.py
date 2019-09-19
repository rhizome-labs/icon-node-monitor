import re
import requests
import time

url = "http://104.196.209.29:9000/api/v1/avail/peer"

response1 = requests.get(url)
data1 = response1.content.decode()

pattern = re.compile(r'\"block_height\"\:([0-9]*)\,\"')
for match1 in re.findall(pattern, data1):
    print(match1)

time.sleep(4)

response2 = requests.get(url)
data2 = response2.content.decode()
for match2 in re.findall(pattern, data2):
    print(match2)

if match1 == match2:
	print("Uh oh. New blocks are not being produced.")
elif match1 < match2:
	print("Yay! New blocks are being produced.")
else:
	print("Something is very, very wrong.")
