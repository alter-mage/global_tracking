import urllib.request
import json
import ssl
import scripts.users

auth_url = 'https://api.lufthansa.com/v1/oauth/token'
track_url = 'https://api.lufthansa.com/v2/cargo/shipment/tracking'

confirmed_status = ['BKG', 'FWB', 'FOH', 'RCS']
transit_status = ['DEP', 'ARR', 'NFD', 'RCF']
delivered_status = ['DLV']

def process_response(track_response):
    cargo_sos = []

    for shipment_status in track_response:
        # print(key)
        # print(track_response[key])
        cargo_info = {
            'doc_number': track_response[shipment_status]['shipment']['shipmentId']['carrierNumericCode']+'-'+track_response['shipmentTrackingStatus']['shipment']['shipmentId']['aWBNumber'],
            'origin': track_response[shipment_status]['booking']['origin'],
            'destination': track_response[shipment_status]['booking']['destination']
        }

        cargo_confirmed_milestones = []
        cargo_transit_milestones = []
        cargo_delivered_milestones = []
        cargo_milestone = {
            'event_airport': track_response['eventAirport'],
            'movement_details': cargo_tracking_status['movementDetails']
        }

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