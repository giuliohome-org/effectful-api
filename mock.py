from effect import Effect, sync_perform, sync_performer, TypeDispatcher, Error
from logic import main_sequence
from api import CreateRequest, UpdateRequest, CloseRequest

# Define mock performers that accept three arguments
@sync_performer
def mock_create_request_performer(dispatcher, intent):
    print("Mock: Creating request...", intent.payload)
    return "mock-request-id"  # Return a fake object ID

@sync_performer
def mock_update_request_performer(dispatcher, intent):
    print(f"Mock: Updating request {intent.request_id} with payload: {intent.payload}")
    # raise Exception("error occurred")
    return {"id": intent.request_id, "mypayload": intent.payload}

@sync_performer
def mock_close_request_performer(dispatcher, intent):
    print(f"Mock: Closing request {intent.request_id}")
    return {"id": intent.request_id, "status": "closed"}

# Create a new TypeDispatcher and add mock performers
mock_dispatcher = TypeDispatcher({
    CreateRequest: mock_create_request_performer,
    UpdateRequest: mock_update_request_performer,
    CloseRequest: mock_close_request_performer,
})



# Run the effect with the mock dispatcher
try:
    result = sync_perform(mock_dispatcher, main_sequence())
    print(f"Mock sequence completed with result: {result}")
except Exception as e:
    print(f"Failed to complete mock sequence: {e}")
