from effect import Effect, sync_perform, Error
from api import CreateRequest, UpdateRequest, CloseRequest


# Define the pure, effectful logic (inspired by Haskell's philosophy: the IO-like sequence is pure, without side effects)
def main_sequence(log):
    # Create the object
    create_effect = Effect(CreateRequest(payload={"name": "New Request", "details": "Some details"}))

    def update_step(request_id):
        update_effect = Effect(UpdateRequest(request_id, payload={"status": "scheduled"}))
        log.info("Updated effect with object id %s", request_id)
        return update_effect.on(success=close_step, error=handle_failure)

    def close_step(updated_response):
        request_id = updated_response["id"]
        log.info("Closing mypayload %s", updated_response["mypayload"])
        close_effect = Effect(CloseRequest(request_id))
        return close_effect.on(error=handle_failure)

    def handle_failure(error):
        log.info(f"Operation failed: {error}")
        return Error(error)

    # Start the sequence: create -> update -> close
    return create_effect.on(success=update_step, error=handle_failure)



