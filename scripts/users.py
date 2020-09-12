import json

users = {
    "qr": [{
        "userHostKey":"TESTHOST",
        "clientId":"ORQRUSER1",
        "clientSecret":"0901ce169c7c960a488e4e1c58d50ca1056eaf01288fef8b718223bf92b58883"
    }],
    "lh": [{
        "userHostKey":"TESTHOST",
        "clientId":"na8va46yrk9yj5v57vmn55ry",
        "clientSecret":"RGD2hCysUdP7A8WXEw84"
    }]
}

def get_qr_user():
    return users['qr'][0]