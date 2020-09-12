import urllib.request
import json
import ssl
import scripts.users

auth_url = 'https://croamisstg.qatarairways.com.qa/cargoapis/api/v1/auth/authorize'
track_url = 'https://croamisstg.qatarairways.com.qa/cargoapis/api/v1/trackShipment'

def get_access():
    user = scripts.users.get_qr_user()
    auth_req = urllib.request.Request(
        auth_url,
        headers={
            'content-type': 'application/json'
        },
        data=bytes(json.dumps(user).encode('utf-8'))
    )

    auth_res = urllib.request.urlopen(auth_req, context=ssl._create_unverified_context())
    auth_data = json.loads(auth_res.read())
    return auth_data['accessToken']

def track_shipment(track_request_data):
    access_token = get_access()

    track_req = urllib.request.Request(
        track_url,
        headers={
            'content-type': 'application/json',
            'Authorization': 'Bearer %s' % (access_token)
        },
        data=bytes(json.dumps(track_request_data).encode('utf-8'))
    )

    track_res = urllib.request.urlopen(track_req, context=ssl._create_unverified_context())
    track_data = json.loads(track_res.read())
    return track_data

