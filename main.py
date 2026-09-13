from datetime import datetime

from checker import check_availability
from config import JOURNEY_DATE
from telegram import send_telegram_message


def extract_status(result):
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


def main():
    print("Starting one-shot multi-city IRCTC availability check...")

    try:
        results = check_availability()
        lines = [
            "🚆 IRCTC Multi-City Seat Update",
            f"Journey date: {JOURNEY_DATE}",
            "",
        ]
        available = []

        for route_name, route_result in results.items():
            lines.append(
                f"🚉 {route_result['train_number']} {route_result['train_name']}"
            )
            lines.append(
                f"{route_result['from_station']} → {route_result['to_station']}"
            )

            for travel_class, result in route_result["classes"].items():
                status = extract_status(result)
                icon = "✅" if is_available(status) else "❌"
                lines.append(f"{icon} {travel_class}: {status}")
                if is_available(status):
                    available.append(
                        f"{route_result['train_number']} {route_result['from_station']}→{route_result['to_station']} {travel_class}: {status}"
                    )
            lines.append("")

        if available:
            lines.append("🎉 AVAILABLE / RAC")
            lines.extend(available)
        else:
            lines.append("ℹ️ No Available/RAC class found right now.")

        message = "\n".join(lines)
        print(f"\n[{datetime.now().isoformat(timespec='seconds')}]\n{message}")
        send_telegram_message(message)

    except Exception as error:
        print(f"[{datetime.now()}] Checker error: {error}")
        raise


if __name__ == "__main__":
    main()
