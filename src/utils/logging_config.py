
import logging

def configure_logging():
    """
    Configure logging settings for the application.
    """
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


