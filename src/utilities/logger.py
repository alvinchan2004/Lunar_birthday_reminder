import logging
import os
from pathlib import Path
from src.config import LOG_FILE_PATH, LOG_PATH

LOGGER_NAME = "MarketPulse"

class Loggable:
    """
    A utility class to facilitate logging and option output like to GUI
    
    How to use:
    1. Inherit this class in your class.
    2. If Output function is necessary, pass the output function to constructor.
    3. Use output_and_log method to log and output messages.
    """
    _is_logging_configured = False

    @classmethod
    def _setup_logging(cls) -> None:
        """Set up logging configuration. It would be call only once in the appication run time.

        Args:
            log_file (str | Path): Path to the log file.
        """
        if cls._is_logging_configured:
            return

        logger = logging.getLogger(LOGGER_NAME)
        logger.setLevel(logging.DEBUG)

        # Create log directory if it doesn't exist
        Path(LOG_PATH).mkdir(parents=True, exist_ok=True)

        # File handler
        fh = logging.FileHandler(LOG_FILE_PATH)
        fh.setLevel(logging.DEBUG)

        # Console handler
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        # Formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        # Clear any existing handlers
        if logger.hasHandlers():
            logger.handlers.clear()

        # Add handlers to logger
        logger.addHandler(fh)
        logger.addHandler(ch)

        cls._is_logging_configured = True

    def __init__(self, module_name: str, output_function=None):
        if not Loggable. _is_logging_configured:
            Loggable._setup_logging()
        self._logger = logging.getLogger(LOGGER_NAME)
        self._output_function = output_function
        self._module = module_name


    def output_and_log(self, msg:str, level=logging.INFO):
        """
        Output the message to both logger and output function if provided.

        Args:
            msg (str): The message to log and output.
            level: Logging level (default: logging.INFO).
        """
        log_msg = f"[{self._module}] {msg}"

        if self._output_function:
            self._output_function(log_msg, level)
        self._logger.log(level, log_msg)