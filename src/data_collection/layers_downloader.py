import requests
import dotenv
import os

dotenv.load_dotenv()
EONET_API_KEY = os.getenv('NASA_API_KEY')

def download_image(image_url, image_path):
    response = requests.get(image_url)
    if response.status_code == 200:
        with open(image_path, 'wb') as f:
            f.write(response.content)
    else:
        print(f"Failed to download image. Status Code: {response.status_code}")


def fetch_layers_for_event(event_id):
    event_url = f"https://eonet.gsfc.nasa.gov/api/v3/events/{event_id}"
    header = {'Authorization': f'Bearer {EONET_API_KEY}'}

    response = requests.get(event_url, headers=header)

    if response.status_code == 200:
        event_data = response.json()

        layers = event_data.get('layers', [])

        for layer in layers:
            image_url = layer.get('image_url', '')
            if image_url:
                image_path = f"../../data/raw/{event_id}_{layer['id']}.jpg"
                download_image(image_url, image_path)
    else:
        print(f"Failed to fetch layers for event {event_id}. Status Code: {response.status_code}")

fetch_layers_for_event('EONET_6418')