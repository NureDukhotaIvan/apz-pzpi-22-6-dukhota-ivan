# config.py

BASE_URL = "http://127.0.0.1:8000/api"
LOGIN_URL = "http://127.0.0.1:8000/api/token/"
REFRESH_URL = "http://127.0.0.1:8000/api/token/refresh/"
SENSORS_URL = f"{BASE_URL}/iot/sensors/"
CAMERAS_URL = f"{BASE_URL}/iot/cameras/"
INCIDENTS_URL = f"{BASE_URL}/action/incidents/"
