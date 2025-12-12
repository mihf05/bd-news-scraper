import logging
from datetime import datetime
from pathlib import Path


def setup_logger(
    logger_name: str,
    log_file_path: str | Path,
    log_level: int,
    log_message_format: str,
) -> logging.Logger:
    """Create and configure a logger object.

    Args:
        logger_name: Name of the logger.
        log_file_path: File path to which logs should be saved.
        log_level: Logging level (DEBUG=10, INFO=20, WARNING=30, ERROR=40, CRITICAL=50).
        log_message_format: Log message format string.

    Returns:
        logging.Logger: Configured logger instance.
        
    Example:
        >>> logger = setup_logger(
        ...     "MyLogger", 
        ...     "logs/app.log", 
        ...     logging.INFO,
        ...     "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        ... )
    """
    logger = logging.getLogger(logger_name)
    
    # Avoid adding multiple handlers if logger already exists
    if logger.handlers:
        return logger

    formatter = logging.Formatter(log_message_format)
    
    # Ensure log directory exists
    log_path = Path(log_file_path)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    
    file_handler = logging.FileHandler(log_file_path, encoding='utf-8')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    logger.setLevel(log_level)

    return logger


def string_to_date(date_str: str) -> datetime:
    """Convert date string to datetime object.
    
    Expected format: DD-MM-YYYY

    Args:
        date_str: Date string in DD-MM-YYYY format.

    Returns:
        datetime: Converted datetime object.
        
    Raises:
        ValueError: If date_str doesn't match the expected format.

    Example:
        >>> string_to_date("21-01-2020")
        datetime.datetime(2020, 1, 21, 0, 0)
    """
    return datetime.strptime(date_str, "%d-%m-%Y")


def date_to_string(date: datetime) -> str:
    """Convert datetime object to formatted string.
    
    Output format: DD-MM-YYYY

    Args:
        date: Input datetime object.

    Returns:
        str: Formatted date string.

    Example:
        >>> from datetime import datetime
        >>> date_to_string(datetime(2020, 1, 21))
        '21-01-2020'
    """
    return date.strftime("%d-%m-%Y")
