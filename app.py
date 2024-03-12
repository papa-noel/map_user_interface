from flask import Flask, request, jsonify, make_response, render_template
import subprocess
import json
import base64
from flask_cors import CORS
import fetch_image

app = Flask(__name__)
CORS(app)  # Enable CORS to allow requests from your frontend

@app.route('/identify-poles', methods=['POST'])
def identify_poles():
    data = request.json
    latitude = data['latitude']
    longitude = data['longitude']
    zoom = data['zoom']
    # Add more parameters as needed

    # Call your Python script with the necessary arguments
    output_bytes = fetch_image.save_image(str(latitude), str(longitude), str(zoom))
    imgResponse = make_response("Response")
    imgResponse.headers["imgBytes"] = "Serve"
    imgResponse.status_code = 0

    
    #result = subprocess.run(['python', 'fetch_image.py', str(latitude), str(longitude), str(zoom)], capture_output=True, text=True)
    #print("After resulkts")


    if imgResponse.status_code == 0:
        b64_bytes = base64.b64encode(output_bytes)
        o = {"data": b64_bytes.decode("utf-8")}
        o_json = json.dumps(o)
        # On success, return whatever result you need to the frontend
        #item = Flask.Response('Hello world!\n', content_type='text/plain')
        return jsonify(o_json)
    else:
        # Handle errors
        return jsonify({'error': "Error"}), 500

if __name__ == '__main__':
    
    app.run(debug=True)
