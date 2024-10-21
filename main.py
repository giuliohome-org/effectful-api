import logging

from effect import sync_perform
from logic import main_sequence
from mock import getDispatcher

logger = logging.getLogger(__name__)


# Run the effect with the mock dispatcher
logging.basicConfig(level=logging.DEBUG)
try:
    mock_dispatcher = getDispatcher(logger)    
    result = sync_perform(mock_dispatcher, main_sequence(logger))
    logger.info(f"Mock sequence completed with result: {result}")
except Exception as e:
    logger.info(f"Failed to complete mock sequence: {e}")
