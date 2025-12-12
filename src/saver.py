import csv
import logging
from datetime import datetime
from pathlib import Path

from config import Config
from models import ItemsModel
from utils import setup_logger


class Saver:
    """Saves processed news articles to disk in CSV format.
    
    Attributes:
        config: Configuration object.
        logger: Logger instance for this saver.
    """

    def __init__(self, config: Config) -> None:
        """Initialize Saver with configuration.
        
        Args:
            config: Configuration object containing settings.
        """
        self.config = config
        self.logger: logging.Logger = setup_logger(
            logger_name="Saver",
            log_file_path=self.config.log_file_path,
            log_level=self.config.log_level,
            log_message_format=self.config.log_message_format,
        )

    def __call__(self, items_in: ItemsModel, current_date: datetime) -> None:
        """Save processed articles to CSV file.
        
        Args:
            items_in: Processed articles to save.
            current_date: Current date being scraped (used for filename).
        """
        if len(items_in) == 0:
            self.logger.info("No items to save.")
            return
            
        output_file_path = self.construct_output_filepath(current_date)
        file_exists = output_file_path.exists()
        
        # Write to CSV using Python's csv module
        with open(output_file_path, 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            
            # Write header if file doesn't exist
            if not file_exists:
                writer.writerow(ItemsModel.COLUMN_NAMES)
            
            # Write all items
            writer.writerows(items_in.to_list())
        
        self.logger.info(f"Saved {len(items_in)} items to: {output_file_path}")

    def construct_output_filepath(self, current_date: datetime) -> Path:
        """Helper function to get output CSV file path.

        The filename format is "<YEAR>.csv"
        For example: 2021.csv

        Args:
            current_date: Current date being scraped.

        Returns:
            Path: Output CSV file path.
        """
        year_str = current_date.strftime("%Y")
        file_name = f"{year_str}.csv"
        return Path(self.config.output_dir) / file_name
