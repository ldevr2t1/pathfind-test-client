#!/usr/bin/env python3

import requests
import json
import sys
from jsoncompare import jsoncompare

if __name__ == '__main__':
    address = str(sys.argv[1])
    test_data = {'testint': 3, 'teststring': 'hi', 'testobj': {'inside': True}}
    response = requests.post('http://' + address + '/v1/')
    assert response.status_code == 200
    uid = response.json()['uid']
    response = requests.put('http://' + address + '/v1/' + str(uid), json=test_data)
    assert response.status_code == 200
    response = requests.get('http://' + address + '/v1/' + str(uid))
    assert response.status_code == 200
    assert jsoncompare.are_same(test_data, response.json())