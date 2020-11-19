#!/usr/bin/env python3
import unittest
import requests
import json
import time
    
def test_token_refresh():
    VERSION='V2.0'
    DEBUG=True
    headers = {'Content-type': 'application/json',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'X-Requested-With': 'XMLHttpRequest'}
    URI="http://159.89.19.111/" + VERSION
    username = 'koha'
    password = '12345678'
    
    s = requests.Session()
    
    # Login via JWT
    login_payload = {'username': username, 'password': password}
    return_value = s.post(URI + '/auth/access_token/', data=json.dumps(login_payload),
        headers=headers
    )
    if not return_value.ok:
        raise Exception("Test failed: status %d, response: %s" % (return_value.status_code,return_value.text))
    
    # Add access token to header. Keep refresh token.
    # NOTE: Header is modified here.
    result = json.loads(return_value.text)
    headers['X-Access-Token'] = '{0}'.format(result['access_token'])
    refresh_token = result['refresh_token']
    key = result['key']
    
    return_value = s.get(URI + '/user/logged_in/',headers=headers)
    if not return_value.ok:
        raise Exception("Test failed: status %d, response: %s" % (return_value.status_code,return_value.text))
    
    while True:
        return_value = s.get(URI + '/user/logged_in/',headers=headers)
        #if not return_value.ok:
        time.sleep(3)
        print("Refreshing token...")
        # Refresh the token.
        headers['X-Access-Token'] = '{0}'.format(refresh_token)
        return_value = s.post(URI + '/auth/access_token/refresh/',headers=headers,data=json.dumps({'key':key}))
        if not return_value.ok:
            raise Exception("Failed to refresh token, response: %s %s" % (return_value.status_code,return_value.text))
        result = json.loads(return_value.text)
        headers['X-Access-Token'] = '{0}'.format(result['access_token'])
        key = result['key']
    
        print("Sleeping...")
        time.sleep(5)
    
    
if __name__ == '__main__':
    import pdb;pdb.set_trace()
    test_token_refresh()
