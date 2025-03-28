import logging
import os
import requests

from boxing.utils.logger import configure_logger


logger = logging.getLogger(__name__)
configure_logger(logger)


RANDOM_ORG_URL = os.getenv("RANDOM_ORG_URL",
                           "https://www.random.org/decimal-fractions/?num=1&dec=2&col=1&format=plain&rnd=new")


def get_random() -> float:
    """Get a random number from random.org.

    This function makes a request to random.org to get a random decimal number
    between 0 and 1 with 2 decimal places.

    Returns:
        float: A random number between 0 and 1.

    Raises:
        RuntimeError: If the request to random.org fails or times out.
        ValueError: If the response from random.org is not a valid number.
    """
    logger.info("Requesting random number from random.org")

    try:
        response = requests.get(RANDOM_ORG_URL, timeout=5)

        # Check if the request was successful
        response.raise_for_status()

        random_number_str = response.text.strip()

        try:
            random_number = float(random_number_str)
            logger.info(f"Successfully retrieved random number: {random_number}")
            return random_number
        except ValueError:
            logger.error(f"Invalid response from random.org: {random_number_str}")
            raise ValueError(f"Invalid response from random.org: {random_number_str}")

    except requests.exceptions.Timeout:
        logger.error("Request to random.org timed out")
        raise RuntimeError("Request to random.org timed out.")

    except requests.exceptions.RequestException as e:
        logger.error(f"Request to random.org failed: {e}")
        raise RuntimeError(f"Request to random.org failed: {e}")