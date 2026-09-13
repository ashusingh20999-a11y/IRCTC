from datetime import datetime

from checker import check_availability
from config import TRAIN_NUMBER, JOURNEY_DATE, FROM_STATION, TO_STATION
from telegram import send_telegram_message


def extract_status(result):
    """Extract a human-readable availability status from common API shapes."""
    if isinstance(result, dict):
        if "error" in result:
            return f"ERROR: {result['error']}"

        data = result.get("data", result)
        if isinstance(data, list):
            if not data:
                return "UNKNOWN"
            return extract_status(data[0])

        if isinstance(data, dict):
            for key in (
                "current_status",
                "availabilityStatus",
                "currentStatus",
                "status",
            ):
                value = data.get(key)
                if value:
                    return str(value)

    return "UNKNOWN"


def is_available(status):
    status = status.upper().strip()
    return status.startswith("AVAILABLE") or status.startswith("RAC")


def build_report(results):
    lines = [
        f"Train {TRAIN_NUMBER} | {FROM_STATION} -> {TO_STATION}",
        f"Journey date: {JOURNEY_DATE}",
    ]

    for travel_class, result in results.items():
        lines.append(f"{travel_class}: {extract_status(result)}")

    return "\n".join(lines)


def main():
    # GitHub Actions already runs this workflow every 5 minutes. Do exactly
    # one API check per workflow run to avoid RapidAPI rate limiting (429).
    print("Starting one-shot IRCTC availability check...")

    try:
        results = check_availability()
        report = build_report(results)
        print(f"\n[{datetime.now().isoformat(timespec='seconds')}]\n{report}")

        available_classes = [
            travel_class
            for travel_class, result in results.items()
            if is_available(extract_status(result))
        ]

        if available_classes:
            message = (
                "IRCTC availability alert\n\n"
                f"{report}\n\n"
                f"Available/RAC class(es): {', '.join(available_classes)}"
            )
            send_telegram_message(message)
        else:
            print("No available/RAC class found. No Telegram alert sent.")

    except Exception as error:
        print(f"[{datetime.now()}] Checker error: {error}")
        raise


if __name__ == "__main__":
    main()
