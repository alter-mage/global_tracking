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

def process_response(track_response):
    cargo_sos = []
    for cargo_tracking_so in track_response['cargoTrackingSOs']:
        cargo_info = {
            'doc_type': cargo_tracking_so['docType'],
            'doc_number': cargo_tracking_so['docNumber']+'-'+cargo_tracking_so['docPrefix'],
            'origin': cargo_tracking_so['origin'],
            'destination': cargo_tracking_so['destination']
        }
        
        cargo_milestones = []
        for cargo_tracking_status in cargo_tracking_so['cargoTrackingMvtStausList']:
            cargo_milestone = {
                'movement_status': cargo_tracking_status['movementStatus'],
                'event_date': cargo_tracking_status['eventDate'],
                'event_airport': cargo_tracking_status['eventAirport'],
                'movement_details': cargo_tracking_status['movementDetails']
            }

            if cargo_tracking_status['movementStatus'] == 'DEP':
                cargo_uldsos = []
                for cargo_tracking_uldso in cargo_tracking_status['cargoTrackingMvtULDSOs']:
                    cargo_uldso = {
                        'uld_owner_code': cargo_tracking_uldso['uldOwnerCode'],
                        'uld_serial_number': cargo_tracking_uldso['uldSerialNumber'],
                        'uld_type': cargo_tracking_uldso['uldType']
                    }
                    cargo_uldsos.append(cargo_uldso)

            cargo_milestones.append(cargo_milestone)
                
    cargo_so = {
        'cargo_info': cargo_info,
        'cargo_milestones': cargo_milestones
    }
    cargo_sos.append(cargo_so)
    return cargo_sos

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
    return process_response(track_data)

    # return {}

