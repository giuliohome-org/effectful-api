from effect import Effect

class NotAsynchronousError(Exception):
    """Performing an effect did not immediately return a value."""

async def async_perform(dispatcher, effect):
    print(f"Processing effect: {effect}")  # Logging for debugging
    # Check if the effect is indeed an Effect instance
    if not isinstance(effect, Effect):
        return effect  # If it's not an Effect, just return the result
    # Dispatch the effect's intent
    performer = dispatcher(effect.intent)
    successes = []
    errors = []
    try:
        performer_result = await performer(dispatcher, effect.intent)
        successes.append(performer_result)
    except Exception as e:  
        errors.append(e)
    else:
        if successes:
            if effect.callbacks:
                success_handler, error_handler = effect.callbacks[0]
                if success_handler is None:
                    return successes[0]
                callback_result = success_handler(successes[0])
                print(f"callback: {callback_result}")
                if isinstance(callback_result, Effect):
                    print(f"callback is an effect: {callback_result}")
                    return await async_perform(dispatcher, callback_result)
                else:
                    print(f"callback is not an effect: {callback_result}")
                    return callback_result
            else:
                return successes[0]
        elif errors:
            if effect.callbacks:
                success_handler, error_handler = effect.callbacks[0]
                if error_handler is None:
                    raise errors[0]
                callback_result = error_handler(errors[0])
                print(f"callback: {callback_result}")
                if isinstance(callback_result, Effect):
                    print(f"callback is an effect: {callback_result}")
                    return await async_perform(dispatcher, callback_result)
                else:
                    print(f"callback is not an effect: {callback_result}")
                    return callback_result
            raise errors[0]
        else:
            raise NotAsynchronousError("Performing %r was not asynchronous!" % (effect,))
