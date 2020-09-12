from flask import Flask, render_template
import scripts.qr_driver
import scripts.afkl_driver
import scripts.lh_driver
import scripts.data

app = Flask(__name__)


@app.route('/')
def index():
    return render_template(
        'Home.html'
    )

@app.route('/track')
def track(track_shipment_id='shipment_id_1'):
    tracking_ids = scripts.data.get_tracking_ids(track_shipment_id)
    # print(tracking_ids)
    track_request_qr = {
        "cargoTrackingRequestSOs": [
        {
            "documentType": "MAWB",
            "documentPrefix": "157",
            "documentNumber": "12345678"
        }
    ]}

    track_request_afkl = '057-91111134'

    track_request_lh = {
        'aWBPrefix': '020',
        'aWBNumber': '52359764'
    }
    
    track_response_qr = scripts.qr_driver.track_shipment(
        track_request_qr
    )

    track_response_afkl = scripts.afkl_driver.track_shipment(
        track_request_afkl
    )

    track_response_lh = scripts.lh_driver.track_lh_shipment(
        track_request_lh
    )
    
    return render_template(
        'index.html',
        track_response_qr=track_response_qr,
        track_response_afkl=track_response_afkl,
        track_response_lh=track_response_lh
    )

if __name__ == '__main__':
    app.run(debug=True)