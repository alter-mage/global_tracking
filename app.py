from flask import Flask, render_template
import scripts.qr_driver

app = Flask(__name__)


@app.route('/')
def index():
    return render_template(
        'index.html'
    )

@app.route('/track')
def track():
    track_request_form_data = {
        "cargoTrackingRequestSOs": [
        {
            "documentType": "MAWB",
            "documentPrefix": "157",
            "documentNumber": "12345678"
        }
    ]}
    track_response = scripts.qr_driver.track_shipment(
            track_request_form_data
        )
    return render_template(
        'index.html', 
        track_response=track_response
    )

if __name__ == '__main__':
    app.run()