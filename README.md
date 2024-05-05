**Overview**
This Python script fetches hourly prices of selected trading pairs from the Gemini exchange API and calculates alerts based on deviations from the average price. It logs the alerts in JSON format.

**Requirements**
Python 3.x
Requests library (pip install requests)

**Usage**
Clone or download this repository.

Run the script (python gemini_alert.py).

**Configuration**

STD_THRESHOLD: Standard deviation threshold for triggering alerts.

WINDOW_SIZE: Size of the window for calculating the moving average.

TOTAL_HOURS: Total number of hours to consider for fetching hourly prices.
