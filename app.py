from flask import Flask, request, jsonify
import subprocess
from flask_cors import CORS
import fetch_image

app = Flask(__name__)
CORS(app)  # Enable CORS to allow requests from your frontend

@app.route('/identify-poles', methods=['POST'])
def identify_poles():
    data = request.json
    print(data) 
    latitude = data['latitude']
    longitude = data['longitude']
    zoom = data['zoom']
    # Add more parameters as needed

    # Call your Python script with the necessary arguments
    print("Flask Running image fetch")
    output_bytes = fetch_image.save_image(str(latitude), str(longitude), str(zoom))
    return output_bytes
    result = subprocess.run(['python', 'fetch_image.py', str(latitude), str(longitude), str(zoom)], capture_output=True, text=True)
    print("After resulkts")

    if result.returncode == 0:
        # On success, return whatever result you need to the frontend
        return jsonify({'message': 'Success', 'data': result.stdout})
    else:
        # Handle errors
        return jsonify({'error': result.stderr}), 500

if __name__ == '__main__':
    
    app.run(debug=True)
