# Exchange Parser

Pet project for parsing USDT - cash exchange rates
from any.exchange using Playwright.

## What it does
- Parses USDT → cash exchange rates
- Parses cash → USDT exchange rates
- Supports multiple cities (Russia / Ukraine)
- Works with manual exchange flow on the website

## Tech stack
- Python 3
- Playwright

## How to run
```bash
pip install -r requirements.txt
playwright install
python main.py
```

## Project status

The project was built as a learning exercise.
The logic may change as the website updates.

## Future improvements
- Better error handling
- Logging instead of print
- Configurable city list
