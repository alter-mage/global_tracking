import urllib.request
import requests
import json
import ssl
import scripts.users

auth_url = 'https://api.lufthansa.com/v1/oauth/token'
track_url = 'https://api.lufthansa.com/v2/cargo/shipment/tracking'

def track_lh_shipment(track_request_data):
    access_token = 'b3btgpxkt2mr6ftwgwwgj73u'
    
    track_filter='?'
    for track_key in track_request_data:
        track_filter += '%s=%s&' % (track_key, track_request_data[track_key])
    track_filter = track_filter[:-1]

    track_req = urllib.request.Request(
        track_url + track_filter,
        headers={
            'content-type': 'application/json',
            'Authorization': 'Bearer %s' % (access_token)
        }
    )
    track_res = urllib.request.urlopen(track_req)
    track_data = json.loads(track_res.read())
    return track_data