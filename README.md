**Overview**
This Python script fetches hourly prices of selected trading pairs from the Gemini exchange API and calculates alerts based on deviations from the average price. It logs the alerts in JSON format.

**Requirements**
Python 3.x
Requests library (pip install requests)

**Usage**
Clone or download this repository.

Run the script (python3 gemini.py).

**Configuration**

STD_THRESHOLD: Standard deviation threshold for triggering alerts.

WINDOW_SIZE: Size of the window for calculating the moving average.

TOTAL_HOURS: Total number of hours to consider for fetching hourly prices.

**How it works**

An alert is triggered whenever the change in price is higher than the threshold

An INFO alert is triggered in this case, a DEBUG alert is also triggered just to log the data periodically every hour.
