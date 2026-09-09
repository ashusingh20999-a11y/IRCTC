import time
from datetime import datetime

from checker import check_availability
from config import (
    TRAIN_NUMBER,
    JOURNEY_DATE,
    FROM_STATION,
    TO_STATION,
    POLL_INTERVAL_SECONDS,
)
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
    print("Starting IRCTC availability checker. Press Ctrl+C to stop.")
    previous_status = {}

    while True:
        try:
            results = check_availability()
            report = build_report(results)
            print(f"\n[{datetime.now().isoformat(timespec='seconds')}]\n{report}")

            for travel_class, result in results.items():
                status = extract_status(result)
                old_status = previous_status.get(travel_class)

                # Notify when a class becomes available/RAC or changes to a new
                # available status. This avoids sending the same alert every poll.
                if is_available(status) and status != old_status:
                    message = (
                        "IRCTC availability alert\n\n"
                        f"{report}\n\n"
                        f"Class {travel_class} is currently available."
                    )
                    send_telegram_message(message)

                previous_status[travel_class] = status

        except Exception as error:
            print(f"[{datetime.now()}] Checker error: {error}")

        time.sleep(POLL_INTERVAL_SECONDS)


if __name__ == "__main__":
    main()
