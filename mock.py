from logging import Logger
from effect import TypeDispatcher
from api import CreateRequest, UpdateRequest, CloseRequest
import asyncio

# Higher-order function dispatcher
def getDispatcher(logger: Logger, token: str):
    async def mock_create_request_performer(dispatcher, intent):
        logger.debug(f"Mock: Creating request... {intent.payload} with token {token}")
        await asyncio.sleep(1)
        # Use the auth token to call the api...
        return "mock-request-id"  # Return a fake object ID

    async def mock_update_request_performer(dispatcher, intent):
        logger.debug(f"Mock: Updating request {intent.request_id} with payload: {intent.payload}")
        await asyncio.sleep(1)
        # raise Exception("error occurred")
        return {"id": intent.request_id, "mypayload": intent.payload}

    async def mock_close_request_performer(dispatcher, intent):
        logger.debug(f"Mock: Closing request {intent.request_id}")
        await asyncio.sleep(1)
        return {"id": intent.request_id, "status": "closed"}

    # Create a new TypeDispatcher and add mock performers
    return TypeDispatcher({
        CreateRequest: mock_create_request_performer,
        UpdateRequest: mock_update_request_performer,
        CloseRequest: mock_close_request_performer,
    })
