# IRCTC Seat Availability Checker configuration
# Copy this file to config.py locally and fill in your own credentials.
# NEVER commit real API keys or Telegram bot tokens.

RAPIDAPI_KEY = "YOUR_RAPIDAPI_KEY"
RAPIDAPI_HOST = "irctc-api3.p.rapidapi.com"

TELEGRAM_BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
TELEGRAM_CHAT_ID = "YOUR_TELEGRAM_CHAT_ID"

TRAIN_NUMBER = "12951"
JOURNEY_DATE = "2026-09-20"  # YYYY-MM-DD; code converts to DD-MM-YYYY for this API
FROM_STATION = "NDLS"
TO_STATION = "BCT"

CLASSES_TO_CHECK = ["SL", "3A", "2A"]
QUOTA = "GN"
POLL_INTERVAL_SECONDS = 300
