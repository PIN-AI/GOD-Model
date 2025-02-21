import logging
import sys
from typing import Optional
from pathlib import Path

class GodNodeLogger:
    def __init__(self, log_file: Optional[str] = None, log_level: int = logging.INFO):
        """Initialize God Node logger with file and console handlers.
        
        Args:
            log_file: Optional path to log file. If None, logs only to console
            log_level: Logging level (default: INFO)
        """
        self.logger = logging.getLogger('god_node')
        self.logger.setLevel(log_level)
        
        # Create formatters
        console_formatter = logging.Formatter('%(levelname)s: %(message)s')
        file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)

        # File handler if log_file specified
        if log_file:
            log_path = Path(log_file)
            log_path.parent.mkdir(parents=True, exist_ok=True)
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(file_formatter)
            self.logger.addHandler(file_handler)

    def debug(self, msg: str) -> None:
        self.logger.debug(msg)

    def info(self, msg: str) -> None:
        self.logger.info(msg)
        
    def warning(self, msg: str) -> None:
        self.logger.warning(msg)

    def error(self, msg: str) -> None:
        self.logger.error(msg)

    def critical(self, msg: str) -> None:
        self.logger.critical(msg)

# Global logger instance
god_logger = GodNodeLogger()
