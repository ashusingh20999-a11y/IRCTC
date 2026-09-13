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


def _format_journey_date(date_value):
    """Convert YYYY-MM-DD to the API's expected DD-MM-YYYY format."""
    parts = str(date_value).split("-")
    if len(parts) == 3 and len(parts[0]) == 4:
        return f"{parts[2]}-{parts[1]}-{parts[0]}"
    return str(date_value)


def check_availability():
    # Verified against the IRCTC API endpoint shown in RapidAPI Code Snippets.
    url = f"https://{RAPIDAPI_HOST}/fetchAvailability.php"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": RAPIDAPI_HOST,
    }

    results = {}
    for travel_class in CLASSES_TO_CHECK:
        payload = {
            "trainNo": TRAIN_NUMBER,
            "sourceStationCode": FROM_STATION,
            "destinationStationCode": TO_STATION,
            "dateOfJourney": _format_journey_date(JOURNEY_DATE),
            "travelClass": travel_class,
            "quota": QUOTA,
        }
        try:
            response = requests.post(url, headers=headers, data=payload, timeout=20)
            response.raise_for_status()
            results[travel_class] = response.json()
        except requests.RequestException as error:
            results[travel_class] = {"error": str(error)}
        except ValueError as error:
            results[travel_class] = {"error": f"Invalid JSON response: {error}"}

    return results
