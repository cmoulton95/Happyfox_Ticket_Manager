import requests
import json
import re
import csv


auth = ('5ffcf3c5a6c441c8b2516d5e3a375595','59b2cfe4716d4752a5a2b3272faf84fd')

def main(tic_id):
    url = 'https://support.productioncloud.io/api/1.1/json/ticket/{}/'.format(tic_id)
    json_data = requests.get(url,auth=auth).json()
    print(json_data['custom_fields'])

main(20540)