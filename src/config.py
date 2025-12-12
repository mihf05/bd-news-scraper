from datetime import datetime, timedelta
import json
import os
from pathlib import Path
from typing import Any

from utils import string_to_date, date_to_string


_ERROR_MSG_INVALID_OUTPUT = "Output path doesn't exist!"
_ERROR_MSG_OUTPUT_NOT_DIR = "Output path must be a directory"


class Config:
    """Holds configuration data from "config.json" file.
    
    Attributes:
        config_file_path: Path to the configuration JSON file.
        configs: Dictionary containing all configuration values.
    """

    def __init__(self, config_file_path: str | Path) -> None:
        """Initialize Config from JSON file.
        
        Args:
            config_file_path: Path to the config.json file.
            
        Raises:
            FileNotFoundError: If config file doesn't exist.
            ValueError: If config file is not a JSON file or output directory is invalid.
        """
        self.config_file_path = Path(config_file_path)
        
        if not self.config_file_path.exists():
            raise FileNotFoundError(f"Config file not found at {self.config_file_path}")
        
        if self.config_file_path.suffix.lower() != '.json':
            raise ValueError(f"Config file at {self.config_file_path} is not a JSON file")
        
        with open(self.config_file_path, encoding='utf-8') as config_fp:
            self.configs: dict[str, Any] = json.load(config_fp)
        
        # Create output directory if it doesn't exist
        output_path = Path(self.output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Create log directory if it doesn't exist
        log_path = Path(self.configs["log_directory"]["value"])
        log_path.mkdir(parents=True, exist_ok=True)

    @property
    def last_scraped_date(self) -> datetime:
        """Last date up to which news articles were scraped.
        
        Returns the last scraped date if available, otherwise returns the start date.
        Date format: DD-MM-YYYY (e.g., 21-01-2010).
        
        Returns:
            datetime: The last scraped date or start date.
        """
        last_date = self.configs["last_scraped_date"]["value"]
        if last_date is not None:
            return string_to_date(last_date)
        return string_to_date(self.configs["start_date"]["value"])

    @property
    def log_level(self) -> int:
        """Log level of Python Logger.

        10 - Log DEBUG and above.
        20 - Log INFO and above.
        30 - Log WARNING and above.
        40 - Log ERROR and above.
        50 - Log CRITICAL and above.
        """
        return self.configs["log_level"]["value"]

    @property
    def log_message_format(self) -> str:
        """Log format for Python logger."""
        return self.configs["log_message_format"]["value"]

    @property
    def time_delta(self) -> timedelta:
        """Number of days whose articles should be fetched together."""
        return timedelta(days=int(self.configs["threshold"]["value"]))

    @property
    def limit(self) -> int:
        """Number of articles to fetch in one request."""
        return self.configs["limit"]["value"]

    @property
    def total(self) -> int:
        """Number of articles scrapped so far."""
        return self.configs["total"]["value"]

    @property
    def max_attempts(self) -> int:
        """Max number of attempts a request can fail before moving on."""
        return self.configs["max_attempts"]["value"]

    @property
    def output_dir(self) -> str:
        """Directory path where news articles are to be saved."""
        return self.configs["output_directory"]["value"]

    @property
    def min_sleep_time(self) -> int:
        """Minimum number of seconds the scraper must sleep in between requests."""
        return self.configs["min_sleep_time"]["value"]

    @property
    def max_sleep_time(self) -> int:
        """Maximum number of days to go without finding a single news article."""
        return self.configs["max_sleep_time"]["value"]

    @property
    def log_file_path(self) -> str:
        """File path to which log messages will be saved.

        The log file will have a timestamp prefix in the format:
        DD-MM-YYYY hh-mm-ss (AM or PM).log
        
        Example: 21-01-2021 11-12-13 AM.log
        
        Returns:
            str: Full path to the log file.
        """
        log_dir = Path(self.configs["log_directory"]["value"])
        
        if not hasattr(self, "log_file_name"):
            timestamp = datetime.now().strftime("%d-%m-%Y %I-%M-%S %p")
            self.log_file_name = f"{timestamp}.log"
        
        return str(log_dir / self.log_file_name)

    def update(self, newly_added: int, last_scrapped_date: datetime) -> None:
        """Update config file with last scraped date and total scraped information.

        Args:
            newly_added: Number of new articles added.
            last_scrapped_date: Last date up to which articles were scraped.
            
        Raises:
            IOError: If unable to write to config file.
        """
        self.configs["total"]["value"] += newly_added
        self.configs["last_scraped_date"]["value"] = date_to_string(last_scrapped_date)
        
        with open(self.config_file_path, "w", encoding='utf-8') as config_fp:
            json.dump(self.configs, config_fp, indent=2, ensure_ascii=False)

    def __repr__(self) -> str:
        """Return string representation of configuration.
        
        Returns:
            str: Formatted configuration details.
        """
        return "\n".join(
            f"{dic['description']}\n\tCurrent Value: {dic['value']}\n"
            for dic in self.configs.values()
        )


if __name__ == "__main__":
    CONFIG_FILE_PATH = "config.json"
    
    config = Config(CONFIG_FILE_PATH)
    print(config)
    config.update(newly_added=10, last_scrapped_date=datetime.now())
