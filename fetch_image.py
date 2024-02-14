from dotenv import load_dotenv, dotenv_values
import os
import requests
import io
from PIL import Image
import json
import hashlib
import hmac
import base64
import urllib.parse as urlparse
import sys

load_dotenv()
API_KEY = os.environ.get("API_KEY")
SECRET = os.environ.get("SECRET")


def sign_url(input_url=None, secret=None):
    """
    https://developers.google.com/maps/digital-signature
    Sign a request URL with a URL signing secret.
    """
    if not input_url or not secret:
        raise Exception("Both input_url and secret are required")

    url = urlparse.urlparse(input_url)
    url_to_sign = url.path + "?" + url.query
    decoded_key = base64.urlsafe_b64decode(secret)
    signature = hmac.new(decoded_key, str.encode(url_to_sign), hashlib.sha1)
    encoded_signature = base64.urlsafe_b64encode(signature.digest())
    original_url = url.scheme + "://" + url.netloc + url.path + "?" + url.query

    return original_url + "&signature=" + encoded_signature.decode()

def save_image(latitude, longitude, zoom, size="640x640", scale=2, key=API_KEY, secret=SECRET):

    # Construct the URL for satellite tile request
    satellite_url = f"https://maps.googleapis.com/maps/api/staticmap?center={latitude},{longitude}&zoom={zoom}&size={size}&scale={scale}&maptype=satellite&key={key}"
    satellite_url = sign_url(satellite_url, secret)

    response = requests.get(satellite_url)

    # Check the response
    if response.status_code == 200:
        # Save the satellite tile image
        img_name = f'satellite_{latitude}_{longitude}_{zoom}_{scale}.png'
        img_path = img_name
        with open(img_path, 'wb') as file:
            file.write(response.content)
        print(f"Satellite tile image saved as '{img_name}'")
    else:
        print(f"Failed to fetch satellite tile. Status code: {response.status_code}")

#def main():
#    save_image()    

if __name__ == "__main__":
    #if len(sys.argv) < 4:
        #print("Usage: python fetch_image.py <latitude> <longitude> <zoom>")
        #sys.exit(1)
    print(len(sys.argv), sys.argv)

    latitude = sys.argv[1]
    longitude = sys.argv[2]
    zoom = sys.argv[3]
    save_image(latitude, longitude, zoom)