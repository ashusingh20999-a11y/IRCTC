# IRCTC Seat Availability Checker

Checks configured train availability through the configured third-party API and sends Telegram alerts.

## GitHub Actions setup

Add these repository Actions secrets under **Settings → Secrets and variables → Actions**:

- `RAPIDAPI_KEY` — your RapidAPI key
- `RAPIDAPI_HOST` — usually `irctc1.p.rapidapi.com`
- `TELEGRAM_BOT_TOKEN` — Telegram bot token
- `TELEGRAM_CHAT_ID` — destination chat ID

The workflow is located at `.github/workflows/irctc-check.yml` and runs every 5 minutes, with a manual `workflow_dispatch` option.

Before relying on alerts, verify the exact response format and endpoint of your selected availability API.

This project is an availability checker and notifier; it does not automate ticket booking or payment.
