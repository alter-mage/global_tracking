import json

data = {
    'shipment_id_1': {
        'qr': {
            "cargoTrackingRequestSOs": [{
                "documentType": "MAWB",
                "documentPrefix": "157",
                "documentNumber": "12345678"
            }]
        },
        'lh': {
            'aWBPrefix': '020',
            'aWBNumber': '52359764'
        },
        'afkl': '057-91111134'
    }
}

def get_tracking_ids(shipment_id):
    return data[shipment_id]