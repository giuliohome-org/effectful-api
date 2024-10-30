from effect import Effect, Error
from api import CreateRequest, UpdateRequest, CloseRequest

# Define the pure, effectful logic (inspired by Haskell's philosophy: the IO-like sequence is pure, without side effects)
def main_sequence(log):
    create_effect = Effect(CreateRequest(payload={"name": "New Request", "details": "Some details"}))

    def update_step(request_id):
        print(f"Updating request with ID: {request_id}")
        update_effect = Effect(UpdateRequest(request_id, payload={"status": "scheduled"}))
        log.info("Updated effect with object id %s", request_id)
        return update_effect.on(success=close_step, error=handle_failure)

    def close_step(updated_response):
        print(f"Closing request with response: {updated_response}")
        request_id = updated_response["id"]
        log.info("Closing request %s", request_id)
        close_effect = Effect(CloseRequest(request_id))
        return close_effect.on(success=lambda _: Effect("Finished"), error=handle_failure)

    def handle_failure(error):
        log.info(f"Operation failed: {error}")
        return Effect(Error(error))

    return create_effect.on(success=update_step, error=handle_failure)

