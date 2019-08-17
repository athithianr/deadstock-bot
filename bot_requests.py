import time
import requests
import json

post_url = 'https://www.deadstock.ca/cart/add.js'

headers = {
    'id': "21448603500629",
}

response = requests.request("POST", post_url, data=headers)
print(response.text)