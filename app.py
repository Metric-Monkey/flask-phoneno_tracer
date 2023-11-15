from flask import Flask, request, render_template
import phonenumbers
from phonenumbers import geocoder, carrier

app = Flask(__name__)

def get_phone_info(number):
    try:
        # Validate the phone number
        parsed_number = phonenumbers.parse(number)
        if not phonenumbers.is_valid_number(parsed_number):
            return {"error": "Invalid phone number"}

        # Geolocation information
        ch_number = phonenumbers.parse(number, "CH")
        geolocation = geocoder.description_for_number(ch_number, "en")

        # Carrier information
        service_number = phonenumbers.parse(number, "RO")
        carrier_info = carrier.name_for_number(service_number, "en")

        return {"geolocation": geolocation, "carrier": carrier_info}

    except phonenumbers.NumberFormatException as e:
        return {"error": f"Error parsing phone number: {e}"}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_phone_info', methods=['POST'])
def process_phone_info():
    number = request.form['phone_number']
    result = get_phone_info(number)
    return render_template('result.html', result=result)

if __name__ == "__main__":
    app.run(debug=True)

