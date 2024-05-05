
"""
    Adding the requests, date time modules
"""
from datetime import datetime
import json
import statistics
import requests

STD_THRESHOLD = 1.0
WINDOW_SIZE = 24
TOTAL_HOURS = 48

def get_all_symbols():
    """
    Fetches all symbols available on the Gemini exchange.
    Returns:
        list: A list of symbols.
    """
    try:
        response = requests.get("https://api.gemini.com/v1/symbols")
        response.raise_for_status()
        symbols = response.json()
        return symbols
    except requests.exceptions.RequestException as error:
        print(f"Error fetching symbols: {error}")
        return None

def fetch_hourly_prices(pair):
    """
    Fetches hourly prices of a trading pair for the last 24 hours.
    Args:
        pair (str): The symbol pair.
    Returns:
        list: Hourly closing prices.
    """
    try:
        response = requests.get(f"https://api.gemini.com/v2/candles/{pair}/1hr")
        response.raise_for_status()
        candles = response.json()[:TOTAL_HOURS]
        return [candle[4] for candle in candles]
    except requests.exceptions.RequestException as error:
        log_error(f"Fetching hourly prices for {pair} failed", error=str(error))
        return None
    except ValueError as error:
        log_error(f"Parsing hourly prices for {pair} failed", error=str(error))
        return None

def calculate_alert(pair):
    """
    Calculates and logs alerts for a given trading pair.
    Args:
        pair (str): The symbol pair.
    Returns:
        None
    """
    try:
        prices = fetch_hourly_prices(pair)
        if not prices or len(prices) < WINDOW_SIZE:
            raise ValueError("Insufficient prices fetched")

        for hour_index in range(WINDOW_SIZE, len(prices)):
            current_hour_prices = prices[hour_index - WINDOW_SIZE:hour_index]
            avg_price = sum(current_hour_prices) / len(current_hour_prices)
            std_dev = statistics.stdev(current_hour_prices)
            curr_price = prices[hour_index]
            dev_value = abs(curr_price - avg_price) / std_dev
            alert = dev_value > STD_THRESHOLD
            if alert:
                log_info({
                    "message": "Alert generated",
                    "pair": pair,
                    "alert": alert,
                    "current_price": curr_price,
                    "avg_price": avg_price,
                    "std_dev": std_dev,
                    "deviation_value": dev_value
                })
    except ValueError as error:
        log_error(f"Calculating alert for {pair} failed", error=str(error))

def log_info(info):
    """
    Logs information in JSON format.
    Args:
        info (dict): A dictionary containing the following keys:
            - message (str): The log message.
            - pair (str): The trading pair.
            - alert (bool): Indicates whether the log level is INFO or DEBUG.
            - current_price (float): The current price.
            - avg_price (float): The average price.
            - std_dev (float): The standard deviation.
            - deviation_value (float): The deviation value.
    Returns:
        None
    """
    log = {
        "timestamp": datetime.now().isoformat(),
        "log_level": "INFO" if info['alert'] else "DEBUG",
        "trading_pair": info['pair'],
        "deviation": info['alert'],
        "data": {
            "message": info['message'],
            "current_price": info['current_price'],
            "average_price": info['avg_price'],
            "standard_deviation": info['std_dev'],
            "price_change_value": info['deviation_value'] * info['std_dev'],
            "deviation_value": info['deviation_value']
        }
    }
    print(json.dumps(log))

def log_error(message, error=None):
    """
    Logs an error message in JSON format.
    Args:
        message (str): The error message to be logged.
        error (str, optional): The error details.
    Returns:
        None
    """
    log = {
        "timestamp": datetime.now().isoformat(),
        "log_level": "ERROR",
        "trading_pair": None,
        "deviation": False,
        "data": {
            "message": message,
            "error": error
        }
    }
    print(json.dumps(log))

def main():
    """
    Entry point of the script.
    Iterates over selected trading pairs and calculates alerts for each pair.
    Returns:
        None
    """
    selected_pairs = ["btcusd"]
    for pair in selected_pairs:
        calculate_alert(pair)

if __name__ == "__main__":
    main()
