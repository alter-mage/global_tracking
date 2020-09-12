import urllib.request
import requests
import json
import ssl
import scripts.users

auth_url = 'https://api.lufthansa.com/v1/oauth/token'
track_url = 'https://api.lufthansa.com/v2/cargo/shipment/tracking?aWBPrefix=020&aWBNumber=52359764'

def track_lh_shipment():
    access_token = 'b3btgpxkt2mr6ftwgwwgj73u'
    print(access_token)

    track_req = urllib.request.Request(
        track_url,
        headers={
            'content-type': 'application/json',
            'Authorization': 'Bearer %s' % (access_token)
        }
    )
    track_res = urllib.request.urlopen(track_req)
    track_data = json.loads(track_res.read())
    return track_data