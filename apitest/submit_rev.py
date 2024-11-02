import sys
import requests
import json

url="http://localhost:15001/submit_review"

if len(sys.argv) > 5:
    print("too many parameters")
    sys.exit()

data = {'user_id': sys.argv[1], 'api_credential': sys.argv[2],
        'reccomandation_id': sys.argv[3], 'evaluation': sys.argv[4]}
ret = requests.post(url, json=data)

if ret.status_code == 200:
    print(ret.json())
else:
    print("error")
