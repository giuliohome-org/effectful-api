import asyncio
from effect import Effect, TypeDispatcher

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
    if not isinstance(effect, Effect):
        return effect  # Base case: if it's a result, return it directly

    # Dispatch the performer for the effect’s intent
    performer = dispatcher(effect.intent)
    if asyncio.iscoroutinefunction(performer):
        # Call the async performer and get the result
        result = await performer(dispatcher, effect.intent)
    else:
        # Call the performer synchronously if it's not async
        result = performer(dispatcher, effect.intent)

    # Check if there are any chained effects via `.on()`
    next_effect = effect.on_success(result) if effect.success_callback else result
    if isinstance(next_effect, Effect):
        # Recursively perform the next effect
        return await perform_async(dispatcher, next_effect)
    return next_effect
