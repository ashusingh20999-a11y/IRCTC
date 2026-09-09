import requests
from config import (
    RAPIDAPI_KEY,
    RAPIDAPI_HOST,
    TRAIN_NUMBER,
    JOURNEY_DATE,
    FROM_STATION,
    TO_STATION,
    CLASSES_TO_CHECK,
    QUOTA,
)


def check_availability():
    url = f"https://{RAPIDAPI_HOST}/api/v1/checkSeatAvailability"
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": RAPIDAPI_HOST,
    }

    results = {}
    for travel_class in CLASSES_TO_CHECK:
        params = {
            "classType": travel_class,
            "fromStationCode": FROM_STATION,
            "toStationCode": TO_STATION,
            "quota": QUOTA,
            "trainNo": TRAIN_NUMBER,
            "date": JOURNEY_DATE,
        }
        try:
            response = requests.get(url, headers=headers, params=params, timeout=15)
            response.raise_for_status()
            results[travel_class] = response.json()
        except requests.RequestException as error:
            results[travel_class] = {"error": str(error)}

    return results
