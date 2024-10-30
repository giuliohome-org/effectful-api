import asyncio
from effect import Effect, Error, TypeDispatcher

# Define an intent to represent the async sleep
class SleepIntent:
    def __init__(self, seconds):
        self.seconds = seconds

# Asynchronous performer using asyncio.sleep directly
async def async_sleep_performer(dispatcher, intent):
    await asyncio.sleep(intent.seconds)
    return f"Slept for {intent.seconds} seconds."

# Create a dispatcher to register our async performer
dispatcher = TypeDispatcher({SleepIntent: async_sleep_performer})

# Recursive perform function to handle async effects with chaining
async def perform_async(dispatcher, effect):
    print(f"Processing effect: {effect}")  # Log for debugging
    if not isinstance(effect, Effect):
        return effect  # If it's not an Effect, return as is

    performer = dispatcher(effect.intent)

    result = await (performer(dispatcher, effect.intent) if asyncio.iscoroutinefunction(performer) else performer(dispatcher, effect.intent))

    # Debug output to check result
    print(f"Result of effect processing: {result}")  # Log the raw result

    if hasattr(result, 'success'):
        if result.success:
            next_effect = effect.on(success=result.callbacks[0][0], error=handle_failure)
            print(f"Next effect determined: {next_effect}")
            return await perform_async(dispatcher, next_effect)
        else:
            return handle_failure(result.error)
    else:
        print(f"Unexpected result format: {result}")
        return handle_failure("Unexpected result format")

def handle_failure(error):
    print(f"Operation failed: {error}")
    return Effect(Error(error))  # Ensure it returns an Effect
