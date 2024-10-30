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

# Custom perform function to handle async performers
async def perform_async(dispatcher, effect):
    performer = dispatcher(effect.intent)
    if asyncio.iscoroutinefunction(performer):
        # Call the async performer directly if it's a coroutine
        return await performer(dispatcher, effect.intent)
    else:
        # Otherwise, call the performer synchronously
        return performer(dispatcher, effect.intent)
