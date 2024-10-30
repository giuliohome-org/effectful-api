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
    print(f"Processing effect: {effect}")
    
    if not isinstance(effect, Effect):
        return effect  # Return directly if it's not an Effect

    performer = dispatcher(effect.intent)

    # Execute the performer
    result = await (performer(dispatcher, effect.intent) if asyncio.iscoroutinefunction(performer) else performer(dispatcher, effect.intent))

    # Check result structure
    if isinstance(result, dict) and "id" in result and "success" in result:
        if result["success"]:
            # Call the next step based on the result
            return await perform_async(dispatcher, result["next_effect"])
        else:
            return handle_failure("Failed to create request")
    else:
        return handle_failure("Unexpected result format")

def handle_failure(error):
    print(f"Operation failed: {error}")
    return Effect(Error(error))  # Ensure it returns an Effect
