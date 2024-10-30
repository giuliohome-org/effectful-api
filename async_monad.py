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
    # Log the current effect being processed
    print(f"Processing effect: {effect}")
    
    # Ensure we're handling an Effect
    if not isinstance(effect, Effect):
        return effect  # If not an effect, return it directly

    # Dispatch the performer for the effect's intent
    performer = dispatcher(effect.intent)
    
    # Check if the performer is a coroutine
    if asyncio.iscoroutinefunction(performer):
        result = await performer(dispatcher, effect.intent)
    else:
        result = performer(dispatcher, effect.intent)

    # Check for next effects
    next_effect = effect.on(success=lambda r: Effect(result), error=lambda e: Effect(Error(e)))
    
    # Log the processing flow
    print(f"Performing next effect: {next_effect}")
    
    # Avoid infinite recursion: check if next_effect is indeed an Effect
    if isinstance(next_effect, Effect):
        return await perform_async(dispatcher, next_effect)

    return result  # Return the final result if there are no further effects
