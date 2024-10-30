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
    print(f"Processing effect: {effect}")  # Logging for debugging
    # Check if the effect is indeed an Effect instance
    if not isinstance(effect, Effect):
        return effect  # If it's not an Effect, just return the result

    # Dispatch the effect's intent
    performer = dispatcher(effect.intent)
    
    # Execute the performer, await if it's a coroutine
    result = await (performer(dispatcher, effect.intent) if asyncio.iscoroutinefunction(performer) else performer(dispatcher, effect.intent))

    # Determine next effect based on the result and call the corresponding handler
    if isinstance(result, Effect):
        next_effect = result.on(success=perform_async, error=handle_failure)
        print(f"Next effect determined: {next_effect}")
        return await perform_async(dispatcher, next_effect)

    return result  # Return the final result if there are no further effects

def handle_failure(error):
    print(f"Operation failed: {error}")
    return Effect(Error(error))  # Ensure it returns an Effect
