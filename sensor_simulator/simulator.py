import requests
import random
import time

API_URL = 'http://127.0.0.1:4000/api/sensors'
SENSOR_IDS = [1, 2, 3]

while True:
    for sensor_id in SENSOR_IDS:
        moisture_level = random.uniform(20.0, 80.0)
        payload = {'moisture_level': moisture_level}
        try:
            response = requests.post(f'{API_URL}/{sensor_id}/moisture', json=payload)
            if response.status_code == 200:
                print(f'Sensor {sensor_id} moisture updated to {moisture_level:.2f}%')
            else:
                print(f'Error updating sensor {sensor_id}: {response.json()}')
        except Exception as e:
            print(f'Exception for sensor {sensor_id}: {e}')
    time.sleep(10)
