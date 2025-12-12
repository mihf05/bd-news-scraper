import logging
import re
from typing import Any

from config import Config
from models import ItemModel, ItemsModel
from utils import setup_logger


class Processor:
    """Processes raw response JSON data from Prothom Alo API.
    
    Attributes:
        config: Configuration object.
        logger: Logger instance for this processor.
    """

    def __init__(self, config: Config) -> None:
        """Initialize Processor with configuration.
        
        Args:
            config: Configuration object containing settings.
        """
        self.config = config
        self.logger: logging.Logger = setup_logger(
            logger_name="Processor",
            log_file_path=self.config.log_file_path,
            log_level=self.config.log_level,
            log_message_format=self.config.log_message_format,
        )

    def __call__(self, items_in: list[dict[str, Any]]) -> ItemsModel:
        """Process raw items into ItemsModel.
        
        Args:
            items_in: List of raw article dictionaries from API.
            
        Returns:
            ItemsModel: Processed and filtered articles.
        """
        self.logger.debug(f"Raw unprocessed items: {len(items_in)}")
        items_out = ItemsModel()

        for raw_item in items_in:
            items_out.add(self.parse_data(raw_item))

        self.logger.debug(f"Filtered processed items: {len(items_out)}")
        return items_out

    def parse_data(self, item: dict[str, Any]) -> ItemModel:
        """Parse article data into ItemModel.

        Args:
            item: Raw news article data dictionary.

        Returns:
            ItemModel: Parsed news article data.
        """
        seo_description, seo_tags = self.parse_seo_data(item)
        
        return ItemModel(
            headline=item.get("headline"),
            subheadline=item.get("subheadline"),
            content=self.construct_content_text(item),
            tags=self.construct_tags_text(item),
            published_at=self.to_unix_timestamp(item.get("published-at", 0)),
            url=item.get("url"),
            seo_description=seo_description,
            seo_tags=seo_tags,
            main_author=item.get("author-name"),
            authors=self.construct_authors_text(item),
            summary=item.get("summary"),
            read_time=int(item.get("read-time", '0')),
            id=item.get("id"),
            sections=self.construct_sections_text(item),
            word_count=item.get("word-count", 0),
            created_at=self.to_unix_timestamp(item.get("created-at", 0)),
            updated_at=self.to_unix_timestamp(item.get("updated-at", 0)),
            first_published_at=self.to_unix_timestamp(item.get("first-published-at", 0)),
            last_published_at=self.to_unix_timestamp(item.get("last-published-at", 0)),
            content_updated_at=self.to_unix_timestamp(item.get("content-updated-at", 0)),
        )

    def to_unix_timestamp(self, timestamp_string: int) -> int:
        """Convert timestamp to UNIX timestamp in seconds.

        Args:
            timestamp_string: Timestamp in milliseconds.

        Returns:
            int: UNIX timestamp in seconds.
        """
        return int(int(timestamp_string) / 1000)

    def construct_authors_text(self, item: dict[str, Any]) -> str | None:
        """Construct comma-separated author names.

        Args:
            item: Raw news article data.

        Returns:
            str | None: Comma-separated author text or None.
        """
        authors = item.get("authors")
        if authors is not None:
            return ",".join(str(author.get("name", "")) for author in authors)
        return None

    def parse_seo_data(self, item: dict[str, Any]) -> tuple[str | None, str | None]:
        """Parse SEO related data and return relevant information.

        Args:
            item: Raw news article data.

        Returns:
            tuple: SEO description and comma-separated keywords.
        """
        if "seo" in item:
            return item.get("meta-description"), item.get("meta-keywords")
        return None, None

    def construct_content_text(self, item: dict[str, Any]) -> str:
        """Extract and clean text content from article cards.
        
        Args:
            item: Raw news article data.
            
        Returns:
            str: Cleaned article content.
        """
        return "".join(
            self.clean_text(element["text"])
            for card in item.get("cards", [])
            for element in card.get("story-elements", [])
            if element.get("type") == "text"
        )

    def construct_tags_text(self, item: dict[str, Any]) -> str | None:
        """Construct tag string.

        Args:
            item: Raw news article data.

        Returns:
            str | None: Comma-separated tags or None.
        """
        tags = item.get("tags")
        if tags is not None:
            tag_names = [tag.get("name") for tag in tags if tag.get("name")]
            return ",".join(tag_names) if tag_names else None
        return None

    def clean_text(self, text: str) -> str:
        """Remove HTML tags from text string.

        Args:
            text: Input text to be cleaned.

        Returns:
            str: Cleaned text.
        """
        cleaner = re.compile(r"<.*?>|&.*?;")
        return re.sub(cleaner, "", text)

    def construct_sections_text(self, item: dict[str, Any]) -> str | None:
        """Construct sections string.

        Args:
            item: Raw news article data.

        Returns:
            str | None: Comma-separated section names or None.
        """
        sections = item.get("sections")
        if sections is not None:
            section_names = [s.get("name") for s in sections if s.get("name")]
            return ",".join(section_names) if section_names else None
        return None
