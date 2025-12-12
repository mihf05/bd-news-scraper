import logging
import time
from datetime import datetime
from typing import Any

import requests
from requests.exceptions import RequestException, Timeout, ConnectionError

from config import Config
from utils import setup_logger


class Requester:
    """Fetches response from Prothom Alo website API.
    
    Attributes:
        config: Configuration object.
        logger: Logger instance for this requester.
    """

    def __init__(self, config: Config) -> None:
        """Initialize Requester with configuration.
        
        Args:
            config: Configuration object containing settings.
        """
        self.config = config
        self.logger: logging.Logger = setup_logger(
            logger_name="Requester",
            log_file_path=self.config.log_file_path,
            log_level=self.config.log_level,
            log_message_format=self.config.log_message_format,
        )
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

    @property
    def url_format(self) -> str:
        """Prothom Alo API url format.

        Four parameters should be provided to use this url which are as follows:
        1. `offset`
        2. `limit`
        3. `start`
        4. `end`
        """
        return (
            "https://www.prothomalo.com/api/v1/advanced-search?"
            + "offset={offset}&limit={limit}&sort=latest-published"
            + "&published-after={start}&published-before={end}"
        )

    def __call__(
        self,
        date_start: datetime,
        date_end: datetime,
        offset: int,
    ) -> dict[str, Any]:
        """Fetch response JSON data from API.

        Fetches news article data published within [date_start, date_end] 
        at the specified offset.

        Args:
            date_start: Minimum date of publication.
            date_end: Maximum date of publication.
            offset: Offset value for pagination.

        Raises:
            Exception: Raised when all request attempts failed.

        Returns:
            dict: Response JSON data.
        """
        for attempt in range(1, self.config.max_attempts + 1):
            try:
                request_url = self.construct_request_url(date_start, date_end, offset)
                response = self.session.get(request_url, timeout=30)
                response.raise_for_status()
                return response.json()
            except (RequestException, Timeout, ConnectionError) as e:
                self.logger.warning(f"Attempt {attempt}: Request failed - {str(e)}")
                if attempt < self.config.max_attempts:
                    self.wait(attempt)
            except ValueError as e:
                self.logger.error(f"JSON decode error: {str(e)}")
                if attempt < self.config.max_attempts:
                    self.wait(attempt)

        raise Exception("All request attempts failed.")

    def wait(self, attempt: int) -> None:
        """Wait a certain amount of time after a request fails.

        The larger the attempt value, the longer we wait.

        Args:
            attempt: Attempt number.
        """
        sleep_time = 30 * attempt
        self.logger.info(f"Attempting {attempt + 1}th time in {sleep_time}s.")
        time.sleep(sleep_time)

    def construct_request_url(
        self,
        date_start: datetime,
        date_end: datetime,
        offset: int
    ) -> str:
        """Construct request URL using appropriate values.

        Args:
            date_start: Earliest published date an article can have.
            date_end: Latest publish date an article can have.
            offset: Amount of offset to use.

        Returns:
            str: Constructed request URL.
        """
        request_url = self.url_format.format(
            offset=offset,
            limit=self.config.limit,
            start=self.date_to_unix_timestamp(date_start),
            end=self.date_to_unix_timestamp(date_end)
        )
        self.logger.info(f"Request URL: {request_url}")
        return request_url

    def date_to_unix_timestamp(self, time: datetime) -> int:
        """Convert time to UNIX timestamp in milliseconds.

        Args:
            time: Time to be converted.

        Returns:
            int: UNIX timestamp in milliseconds.
        """
        return int(time.timestamp() * 1000)

    def __del__(self) -> None:
        """Close the session when the object is destroyed."""
        if hasattr(self, 'session'):
            self.session.close()
