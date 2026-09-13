import requests
from config import RAPIDAPI_KEY, RAPIDAPI_HOST, ROUTES, CLASSES_TO_CHECK, JOURNEY_DATE, QUOTA


def _format_journey_date(date_value):
    parts = str(date_value).split("-")
    if len(parts) == 3 and len(parts[0]) == 4:
        return f"{parts[2]}-{parts[1]}-{parts[0]}"
    return str(date_value)


def check_availability():
    url = f"https://{RAPIDAPI_HOST}/fetchAvailability.php"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": RAPIDAPI_HOST,
    }

    results = {}
    for route in ROUTES:
        route_key = route["name"]
        results[route_key] = {
            "train_number": route["train_number"],
            "train_name": route.get("train_name", ""),
            "from_station": route["from_station"],
            "to_station": route["to_station"],
            "classes": {},
        }

        for travel_class in CLASSES_TO_CHECK:
            payload = {
                "trainNo": route["train_number"],
                "sourceStationCode": route["from_station"],
                "destinationStationCode": route["to_station"],
                "dateOfJourney": _format_journey_date(JOURNEY_DATE),
                "travelClass": travel_class,
                "quota": QUOTA,
            }
            try:
                response = requests.post(url, headers=headers, data=payload, timeout=20)
                response.raise_for_status()
                results[route_key]["classes"][travel_class] = response.json()
            except requests.RequestException as error:
                results[route_key]["classes"][travel_class] = {"error": str(error)}
            except ValueError as error:
                results[route_key]["classes"][travel_class] = {
                    "error": f"Invalid JSON response: {error}"
                }

    return results
