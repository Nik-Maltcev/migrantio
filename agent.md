# Project: Migrant Info Bot

## Overview
This project is a Telegram bot designed to help migrants by providing structured information about various countries. Users can navigate through countries and specific categories (e.g., Medicine, Visas, Housing, Finances) to find relevant information. The bot also offers subscription plans.

## Tech Stack
- **Language:** Python 3.12.12
- **Library:** `python-telegram-bot` v20.7
- **Testing:** `pytest`, `pytest-asyncio`
- **Deployment:** Railway

## File Structure
- `src/`
  - `bot.py`: The main entry point of the application. Contains all the bot logic, command handlers, and callback query handlers.
- `tests/`
  - `test_bot.py`: Unit tests for the bot's functions using `pytest` and `unittest.mock`.
- `Procfile`: Defines the worker process for Railway deployment (`worker: python src/bot.py`).
- `runtime.txt`: Specifies the Python version (`python-3.12.12`).
- `requirements.txt`: Lists project dependencies.

## Setup & Development

### Prerequisites
- Python 3.12
- A Telegram Bot Token (obtainable from @BotFather)

### Installation
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Bot
1. Set the `TELEGRAM_BOT_TOKEN` environment variable.
2. Run the bot:
   ```bash
   python src/bot.py
   ```

### Running Tests
Execute tests using `pytest`. Ensure the current directory is in `PYTHONPATH`:
```bash
PYTHONPATH=. pytest tests/test_bot.py
```
Or simply:
```bash
pytest
```
(if your environment is configured to find the `src` module).

## Key Features & Logic

### Navigation
The bot uses `InlineKeyboardMarkup` for navigation.
- **Main Menu:** Offers options to "Choose Country", "Buy Subscription", and "Info".
- **Countries:** Displays a list of supported countries (Italy, Spain, Greece, Cyprus).
- **Categories:** After selecting a country, users can choose a category (Medicine, Visas, Housing, Finances).
- **Content:** Displays information for the selected country and category.

### Callback Data
The bot uses prefixed callback data to route user actions:
- `menu_`: For main menu navigation (e.g., `menu_countries`, `menu_subscription`).
- `country_`: For selecting a country (e.g., `country_Italy`).
- `cat_`: For selecting a category (e.g., `cat_Italy|Medicine`).
- `back_`: Not actively used in the current simplified logic but reserved for back navigation.

### Subscriptions
Placeholder logic exists for displaying subscription plans and prices.

## Environment Variables
- `TELEGRAM_BOT_TOKEN`: Required. The API token for the Telegram bot.

## Deployment
The project is configured for deployment on Railway.
- `Procfile` defines the `worker` process.
- `runtime.txt` ensures the correct Python version is used.
