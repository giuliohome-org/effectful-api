from effect import Effect, Error
from api import CreateRequest, UpdateRequest, CloseRequest

# Define the pure, effectful logic (inspired by Haskell's philosophy: the IO-like sequence is pure, without side effects)
def main_sequence(log):
    create_effect = Effect(CreateRequest(payload={"name": "New Request", "details": "Some details"}))

    async def handle_update(request_id):
        log.info(f"Request created with ID: {request_id}")
        update_effect = Effect(UpdateRequest(request_id, payload={"status": "scheduled"}))
        return update_effect.on(success=handle_close, error=handle_failure)

    async def handle_close(updated_response):
        log.info(f"Updated response: {updated_response}")
        request_id = updated_response.get("id")
        close_effect = Effect(CloseRequest(request_id))
        return close_effect.on(success=lambda _: Effect("Finished"), error=handle_failure)

    def handle_failure(error):
        log.info(f"Operation failed: {error}")
        return Effect(Error(error))

    return create_effect.on(success=handle_update, error=handle_failure)

