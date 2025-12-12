from dataclasses import dataclass, field
from typing import List, Optional


@dataclass(slots=True, kw_only=True)
class ItemModel:
    """Holds information related to a single news article.
    
    Attributes:
        All attributes default to None and represent various metadata
        about a news article from Prothom Alo.
    """

    headline: Optional[str] = None
    subheadline: Optional[str] = None
    content: Optional[str] = None
    tags: Optional[str] = None
    published_at: Optional[int] = None
    created_at: Optional[int] = None
    updated_at: Optional[int] = None
    last_published_at: Optional[int] = None
    first_published_at: Optional[int] = None
    content_updated_at: Optional[int] = None
    seo_description: Optional[str] = None
    seo_tags: Optional[str] = None
    main_author: Optional[str] = None
    authors: Optional[str] = None
    url: Optional[str] = None
    read_time: Optional[int] = None
    summary: Optional[str] = None
    sections: Optional[str] = None
    id: Optional[str] = None
    word_count: Optional[int] = None

    def to_list(self) -> List:
        """Convert article data to a list format.
        
        Returns:
            List: Article data in list format matching COLUMN_NAMES order.
        """
        return [
            self.id,
            self.headline,
            self.subheadline,
            self.summary,
            self.content,
            self.main_author,
            self.authors,
            self.url,
            self.read_time,
            self.seo_description,
            self.seo_tags,
            self.tags,
            self.sections,
            self.word_count,
            self.published_at,
            self.first_published_at,
            self.last_published_at,
            self.created_at,
            self.updated_at,
            self.content_updated_at,
        ]


class ItemsModel:
    """Holds data for multiple news articles in a list.
    
    Attributes:
        COLUMN_NAMES: List of column names for CSV export.
        items: List of ItemModel instances.
    """

    COLUMN_NAMES: List[str] = [
        "text_id",
        "text_headline",
        "text_subheadline",
        "text_summary",
        "text_content",
        "text_main_author",
        "text_authors",
        "text_url",
        "int_read_time",
        "text_seo_description",
        "text_seo_tags",
        "text_tags",
        "text_sections",
        "int_word_count",
        "date_published",
        "date_first_published_at",
        "date_last_published_at",
        "date_created_at",
        "date_updated_at",
        "date_content_updated_at",
    ]

    def __init__(self) -> None:
        """Initialize an empty ItemsModel."""
        self.items: List[ItemModel] = []

    def add(self, item: ItemModel) -> None:
        """Add an item if it meets acceptance criteria.
        
        Args:
            item: News article data to add.
        """
        if self.is_acceptable(item):
            self.items.append(item)

    def __len__(self) -> int:
        """Return the number of parsed articles.
        
        Returns:
            int: Number of items in the collection.
        """
        return len(self.items)

    def is_acceptable(self, item: ItemModel) -> bool:
        """Check whether an item is acceptable for inclusion.

        An item is acceptable if it has a non-null and non-empty 
        headline and content.

        Args:
            item: News article data to validate.

        Returns:
            bool: True if the item should be added, False otherwise.
        """
        return (
            item.headline is not None 
            and item.content is not None 
            and len(item.headline) > 0 
            and len(item.content) > 0
        )

    def to_list(self) -> List:
        """Convert all items to list format.
        
        Returns:
            List: List of lists containing article data.
        """
        return [item.to_list() for item in self.items]
