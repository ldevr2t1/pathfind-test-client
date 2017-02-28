#!/usr/bin/env python3

import requests
import sys
from jsoncompare import jsoncompare

def check_requests(requests, uid, expected):
    response = requests.get('http://' + address + '/v1/' + str(uid))
    assert response.status_code == 200
    assert jsoncompare.are_same(expected, response.json())

if __name__ == '__main__':
    address = str(sys.argv[1])
    test_data = {'testint': 3, 'teststring': 'hi', 'testobj': {'inside': True}}
    bad_data = '}}}}}}}}}}'

    # Make sure the get request works on the root.
    assert requests.get('http://' + address + '/v1/').status_code == 200

    # Make sure getting from a non-existing uid doesn't work.
    assert requests.get('http://' + address + '/v1/' + 'badtest').status_code == 404

    # Attempt to post to the root to create a UID
    response = requests.post('http://' + address + '/v1/')
    assert response.status_code == 200
    uid = response.json()['uid']

    # Attempt to put non-JSON data to the UID, expecting failure.
    assert requests.put('http://' + address + '/v1/' + str(uid), data=bad_data).status_code == 400

    # Put legitimate JSON data into the provided UID.
    assert requests.put('http://' + address + '/v1/' + str(uid), json=test_data).status_code == 200
    # Ensure it was updated correctly.
    check_requests(requests, uid, test_data)

    # Delete the UID before testing post.
    assert requests.delete('http://' + address + '/v1/' + str(uid)).status_code == 200

    # Attempt to post to a deleted UID.
    assert requests.post('http://' + address + '/v1/' + str(uid), json=test_data).status_code == 404

    # Attempt to post to the root to create a UID
    response = requests.post('http://' + address + '/v1/')
    assert response.status_code == 200
    uid = response.json()['uid']

    # Attempt to post non-JSON data to the UID, expecting failure.
    assert requests.post('http://' + address + '/v1/' + str(uid), data=bad_data).status_code == 400

    # Post legitimate JSON data into the provided UID.
    assert requests.post('http://' + address + '/v1/' + str(uid), json=test_data).status_code == 200
    # Ensure it was updated correctly.
    check_requests(requests, uid, test_data)

    # Delete the POST test UID.
    assert requests.delete('http://' + address + '/v1/' + str(uid)).status_code == 200

    # Try to delete a non-existing UID.
    assert requests.delete('http://' + address + '/v1/' + str(uid)).status_code == 404

    # Attempt to get from a non-existing UID that existed before.
    assert requests.get('http://' + address + '/v1/' + str(uid)).status_code == 404