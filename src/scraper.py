import logging
import time
from collections.abc import Generator
from datetime import datetime
from random import randint

from config import Config
from processor import Processor
from requester import Requester
from saver import Saver
from utils import setup_logger, date_to_string


class Scraper:
    """Scrapes news articles from Prothom Alo website.
    
    This scraper fetches articles from https://www.prothomalo.com/ using their API,
    processes the data, and saves it to CSV files.
    
    Attributes:
        config: Configuration object.
        logger: Logger instance for this scraper.
        requester: HTTP requester for API calls.
        processor: Data processor.
        saver: File saver.
    """

    def __init__(self, config_file_path: str) -> None:
        """Initialize Scraper with configuration.
        
        Args:
            config_file_path: Path to the config.json file.
        """
        self.config = Config(config_file_path)
        self.logger: logging.Logger = setup_logger(
            logger_name="Scraper",
            log_file_path=self.config.log_file_path,
            log_level=self.config.log_level,
            log_message_format=self.config.log_message_format,
        )
        self.requester = Requester(self.config)
        self.processor = Processor(self.config)
        self.saver = Saver(self.config)

    def begin(self) -> None:
        """Initiate scraping procedure."""
        self.logger.info("Starting scraping process...")
        
        for date_start in self.date_iterable():
            date_end = date_start + self.config.time_delta
            date_range_string = self.construct_date_range_string(date_start, date_end)

            try:
                self.logger.info(f"Working date range: {date_range_string}")
                self.fetch_articles_in_date_range(date_start, date_end)
            except Exception as e:
                self.logger.warning(f"No articles in {date_range_string}: {str(e)}")
                
        self.logger.info("Scraping process completed.")

    def construct_date_range_string(
        self, 
        date_start: datetime, 
        date_end: datetime
    ) -> str:
        """Construct date range string for logging.

        Example: "01-01-2020 to 02-01-2020"

        Args:
            date_start: Starting date.
            date_end: Ending date.

        Returns:
            str: Formatted date range string.
        """
        string_start = date_to_string(date_start)
        string_end = date_to_string(date_end)
        return f"{string_start} to {string_end}"

    def fetch_articles_in_date_range(
        self, 
        date_start: datetime, 
        date_end: datetime
    ) -> None:
        """Fetch articles within date_start and date_end.

        Args:
            date_start: Earliest date of publication.
            date_end: Latest date of publication.

        Raises:
            Exception: Raised if response object is None or invalid.
        """
        for offset in self.offset_iterable():
            response = self.requester(date_start, date_end, offset)

            if response.get("total", 0) == 0 or len(response.get("items", [])) == 0:
                self.logger.info("Response total is 0. Exiting loop.")
                break

            processed_items = self.processor(response["items"])
            self.saver(processed_items, date_start)
            
            self.config.update(
                newly_added=len(processed_items),
                last_scrapped_date=date_end
            )

            self.logger.info(f"Total scraped: {self.config.total}")

    def random_sleep(self) -> None:
        """Sleep for a random amount of time.
        
        Sleep duration is between config.min_sleep_time and config.max_sleep_time.
        """
        sleep_time = randint(
            self.config.min_sleep_time,
            self.config.max_sleep_time
        )
        self.logger.info(f"Sleeping for {sleep_time} seconds")
        time.sleep(sleep_time)

    def date_iterable(self) -> Generator[datetime, None, None]:
        """Create a workable date range iterable.

        Workable date range always starts at config.last_scraped_date and 
        ends at datetime.now().

        Yields:
            datetime: Current date being scraped.
        """
        current_date = self.config.last_scraped_date

        while current_date < datetime.now():
            yield current_date
            current_date += self.config.time_delta

        self.logger.info("Reached current date. Exiting.")

    def offset_iterable(self) -> Generator[int, None, None]:
        """Create an offset iterable that increases offset value.

        The amount of offset increase is determined by config.limit.

        Yields:
            int: Current offset value.
        """
        offset = 0

        while True:
            yield offset
            offset += self.config.limit


if __name__ == "__main__":
    scraper = Scraper("config.json")
    scraper.begin()
