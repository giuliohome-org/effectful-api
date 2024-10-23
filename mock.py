import time
from logging import Logger
from effect import Effect, sync_performer, TypeDispatcher, Error
from logic import main_sequence
from api import CreateRequest, UpdateRequest, CloseRequest

# higher-order function dispatcher
def getDispatcher(logger: Logger, token: str):
    @sync_performer
    def mock_create_request_performer(dispatcher, intent):
        logger.debug(f"Mock: Creating request... {intent.payload} with token {token}")
        time.sleep(1)
        # use the auth token to call the api...
        return "mock-request-id"  # Return a fake object ID

    @sync_performer
    def mock_update_request_performer(dispatcher, intent):
        logger.debug(f"Mock: Updating request {intent.request_id} with payload: {intent.payload}")
        time.sleep(1)
        # raise Exception("error occurred")
        return {"id": intent.request_id, "mypayload": intent.payload}

    @sync_performer
    def mock_close_request_performer(dispatcher, intent):
        logger.debug(f"Mock: Closing request {intent.request_id}")
        return {"id": intent.request_id, "status": "closed"}

    # Create a new TypeDispatcher and add mock performers
    return TypeDispatcher({
        CreateRequest: mock_create_request_performer,
        UpdateRequest: mock_update_request_performer,
        CloseRequest: mock_close_request_performer,
    })
