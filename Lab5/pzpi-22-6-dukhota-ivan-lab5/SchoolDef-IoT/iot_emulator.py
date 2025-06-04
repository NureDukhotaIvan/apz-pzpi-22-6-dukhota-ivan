import requests
import random
import time
from config import BASE_URL, LOGIN_URL, REFRESH_URL, SENSORS_URL, CAMERAS_URL, INCIDENTS_URL

access_token = None
refresh_token = None

CAMERA_LOCATIONS = {
    "Concert Hall": None,
    "Canteen": None,
    "PE class": None,
    "Main Entrance": None,
    "Main Hall": None
}

def authenticate(email, password):
    global access_token, refresh_token
    response = requests.post(LOGIN_URL, json={"email": email, "password": password})
    if response.status_code == 200:
        tokens = response.json()
        access_token = tokens["access"]
        refresh_token = tokens["refresh"]
        print("Успішна авторизація.")
    else:
        raise Exception("Авторизація не вдалася: " + response.text)


def refresh_access_token():
    global access_token
    response = requests.post(REFRESH_URL, json={"refresh": refresh_token})
    if response.status_code == 200:
        access_token = response.json()["access"]
        print("Access-токен оновлено.")
    else:
        print("Неможливо оновити токен:", response.text)
        authenticate()


def get_headers():
    return {"Authorization": f"Bearer {access_token}"}


def fetch_cameras():
    response = requests.get(CAMERAS_URL, headers=get_headers())
    if response.status_code == 401:
        refresh_access_token()
        return fetch_cameras()
    elif response.status_code == 200:
        for camera in response.json():
            location = camera.get("location")
            if location in CAMERA_LOCATIONS:
                CAMERA_LOCATIONS[location] = camera["id"]
        print("Камери завантажені.")
    else:
        raise Exception("Не вдалося отримати камери: " + response.text)


def fetch_sensors():
    response = requests.get(SENSORS_URL, headers=get_headers())
    if response.status_code == 401:
        refresh_access_token()
        return fetch_sensors()
    elif response.status_code == 200:
        return response.json()
    else:
        raise Exception("Не вдалося отримати сенсори: " + response.text)


def create_incident(sensor, camera_id):
    data = {
        "type": sensor["type"],
        "description": f"Було помічено {sensor['type']} у приміщенні: {sensor['location']}",
        "severity": random.randint(1, 5),
        "sensor": sensor["id"],
        "camera": camera_id,
        "reported": True
    }
    response = requests.post(INCIDENTS_URL, json=data, headers=get_headers())
    if response.status_code == 401:
        refresh_access_token()
        return create_incident(sensor, camera_id)
    elif response.status_code == 201:
        print("Інцидент створено успішно.")
    else:
        print("Помилка при створенні інциденту:", response.text)


def main():
    email = input("Введіть email: ")
    password = input("Введіть пароль: ")

    authenticate(email, password)
    fetch_cameras()

    while True:
        sensors = fetch_sensors()
        for sensor in sensors:
            value = random.randint(1, 10000)
            print(f"Sensor {sensor['id']} ({sensor['type']}, {sensor['location']}) -> {value}")
            if value > 9500:
                camera_id = CAMERA_LOCATIONS.get(sensor["location"])
                create_incident(sensor, camera_id)
                print("Симулятор завершив роботу (інцидент зафіксовано).")
                return
        time.sleep(1)


if __name__ == "__main__":
    main()
