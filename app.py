from flask import Flask, render_template
import scripts.qr_driver
import scripts.afkl_driver

app = Flask(__name__)


@app.route('/')
def index():
    return render_template(
        'index.html'
    )

@app.route('/track')
def track():
    track_request_qr = {
        "cargoTrackingRequestSOs": [
        {
            "documentType": "MAWB",
            "documentPrefix": "157",
            "documentNumber": "12345678"
        }
    ]}

    track_request_afkl = '057-91111134'
    
    track_response_qr = scripts.qr_driver.track_shipment(
        track_request_qr
    )

    track_response_afkl = scripts.afkl_driver.track_shipment(
        track_request_afkl
    )
    
    return render_template(
        'index.html',
        track_response_qr=track_response_qr,
        track_response_afkl=track_response_afkl
    )

if __name__ == '__main__':
    app.run()