import sys
import requests
import json

url="http://localhost:15001/get_past_reccomandations"

if len(sys.argv) > 3:
    print("too many parameters")
    sys.exit()

data = {'user_id': sys.argv[1], 'api_credential': sys.argv[2]}
print(data['user_id'])
ret = requests.post(url, json=data)

if ret.status_code == 200:
    print(ret.json())
else:
    print("error")
