import urllib.request
import json
import ssl
import scripts.users
import base64
from flask import request

auth_url = 'https://api-ute2-ext.airfranceklm.com/cargo/tracking/oauth'
track_url = 'https://api-ute2-ext.airfranceklm.com/cargo/tracking/v2/public/shipments'

confirmed_status = ['BKG', 'FWB', 'FOH', 'RCS']
transit_status = ['DEP', 'ARR', 'NFD', 'RCF']
delivered_status = ['DLV']

def get_access():
    user = scripts.users.get_afkl_user()
    user_base64 = base64.b64encode(
        ('%s:%s' % (user['username'], user['password'])).encode('ascii')
    ).decode('utf-8')
    
    auth_req = urllib.request.Request(
        auth_url,
        headers={
            'content-type': 'application/x-www-form-urlencoded',
            'Authorization': 'Basic %s' % (user_base64),
            'Cookie': 'BCSI-CS-5f9302ec8120e41e=1; CLID_cgobkgap_xte_=CZzuipnN+rvxhrxMBWqJMCuED4zhyxv+OKey2m8bbWli6iRF8aNLVLhsZ5RED9Wkh68oMfAAAAAB; BCSI-CS-95da4b98f8f01d25=1; BCSI-CS-7c98ac7721150115=1; BCSI-CS-f91d1304096ea5a1=1'
        },
        data = 'grant_type=client_credentials'.encode('utf8')
    )

    auth_res = urllib.request.urlopen(auth_req, context=ssl._create_unverified_context())
    auth_data = json.loads(auth_res.read())
    return auth_data['access_token']

def process_response(track_response):
    cargo_sos = []
    for shipment in track_response['Shipments']:
        cargo_info = {
            'doc_number': shipment['Shipment']['AirWaybillNumber'],
            'origin': shipment['Shipment']['OriginDestination']['DepartureLocation'],
            'destination': shipment['Shipment']['OriginDestination']['ArrivalLocation'],
            'stage': {
                'phase': shipment['Shipment']['ShipmentStage']['Phase'],
                'status': shipment['Shipment']['ShipmentStage']['Status']
            }
        }

        cargo_confirmed_milestones = []
        cargo_transit_milestones = []
        cargo_delivered_milestones = []
        for cargo_event in shipment['Milestones']['Events']:
            cargo_milestone = {
                'event_airport': cargo_event['EventLocation']
            }

            if 'EventActualTime' in cargo_event:
                cargo_milestone['event_date'] = cargo_event['EventActualTime']

            if any(cargo_event['EventCode'] in status for status in ['DEP', 'ARR']):
                cargo_uldsos = [{
                    'uld_serial_number': cargo_event['TransportIdentifier'],
                    'uld_type': cargo_event['ModeCodeDescription']
                }]

            if any(cargo_event['EventCode'] in status for status in confirmed_status):
                cargo_confirmed_milestones.append(cargo_milestone)

            if any(cargo_event['EventCode'] in status for status in transit_status):
                cargo_transit_milestones.append(cargo_milestone)

            if any(cargo_event['EventCode'] in status for status in delivered_status):
                cargo_delivered_milestones.append(cargo_milestone)

        cargo_so = {
            'cargo_info': cargo_info,
            'cargo_confirmed_milestones': cargo_confirmed_milestones,
            'cargo_transit_milestones': cargo_transit_milestones,
            'cargo_delivered_milestones': cargo_delivered_milestones
        }
        cargo_sos.append(cargo_so)
    return cargo_sos


def track_shipment(track_request_data):
    access_token = get_access()

    req_awb = '/%s' % (track_request_data)
    req_filters = '?expand=shipment-characteristics,milestones'
    track_req = urllib.request.Request(
        track_url + req_awb + req_filters,
        headers={
            'content-type': 'application/json',
            'Authorization': 'Bearer %s' % (access_token)
        }
    )

    track_res = urllib.request.urlopen(track_req, context=ssl._create_unverified_context())
    track_data = json.loads(track_res.read())
    # process_response(track_data)
    return process_response(track_data)