import requests
import logging


def health_check_api():
    url = "https://apikanban.bizmatic.id/monitoring/v1/ping/39816822-9405-48BC-A11E-C6A1683AE702"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)

        # Log the status code and response text
        logging.info(f"Health Check: {response.status_code}")
    except requests.RequestException as e:
        logging.error(f"An error occurred: {e}")
