import logging
import asyncio

from effect import sync_perform
from logic import main_sequence
from mock import getDispatcher

from async_monad import perform_async

logger = logging.getLogger("observable-activity")
token="<secret>"
logging.basicConfig(level=logging.DEBUG)

# Run the effect with the mock dispatcher
# Testing the Effect with asyncio
async def main():
    try:
        mock_dispatcher = getDispatcher(logger, token)    
        result = await perform_async(mock_dispatcher, main_sequence(logger))
        logger.info(f"Mock sequence completed with result: {result}")
    except Exception as e:
        logger.info(f"Failed to complete mock sequence: {e}")

# Run the main async function
asyncio.run(main())
