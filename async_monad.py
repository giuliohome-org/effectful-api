import asyncio
from effect import Effect

async def async_task(future, result):
    # Simulate some processing
    await asyncio.sleep(1)  # This simulates a delay in processing
    # Set the result of the future
    future.set_result(result)

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
        perfresult = await performer(dispatcher, effect.intent)
        successes.append(perfresult)
    except Exception as e:  
        errors.append(e)
    if effect.callbacks:
        callback_result = effect.callbacks[0][0](perfresult)
        print(f"callback: {callback_result}")
        if isinstance(callback_result, Effect):
            print(f"callback is an effect: {callback_result}")
            return await async_perform(dispatcher, callback_result)
        else:
            print(f"callback is not an effect: {callback_result}")
            await asyncio.sleep(1)
            return callback_result
    else:
        if successes:
            return successes[0]
        elif errors:
            raise errors[0]
        else:
            raise NotAsynchronousError("Performing %r was not asynchronous!" % (effect,))
