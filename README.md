# When You Have Python but Want a Taste of Haskell

Welcome to **Effect-Based Workflow Madness**! 🎢 This repo is for those moments when you’re writing Python, but deep down, you’re craving that functional programming flair... without actually jumping into Haskell's deep waters.

## What Is This Sorcery? 🧙‍♂️

Ever wanted to turn your simple Python scripts into a data-driven workflow engine, just for kicks? Well, this example does just that. We use the `effect` library to string together actions like creating, updating, and closing a request... but without actually doing anything. That's right—it's all mock data, no real HTTP calls, and a lot of imagination!

Think of it as a **choose-your-own-adventure book**, but for API calls:
1. **Create a request** (e.g., "New request created!")
2. **Update the request** (e.g., "Request status: sheduled.")
3. **Close the request** (e.g., "Request is now officially over.")

All the magic happens without talking to any servers—because why involve the real world when you can live in a fantasy?

## Prerequisites 📚

- Python 3.8+ (For when Python 2 is too passé)
- `effect` library (`pip install effect`) 

## How Does It Work? 🤔

1. **Define Intents**: Fancy term for "pretend actions":
   - `CreateRequest`: "I wish for a request."
   - `UpdateRequest`: "Make it better, or just... different."
   - `CloseRequest`: "We're done here."

2. **Mock Performers**: The actors in our play, performing without real effort:
   - `mock_create_request_performer`: Pretends to create something. Returns `"mock-request-id"` like it's proud of it.
   - `mock_update_request_performer`: Acts like it updated something. Even prints out the fake payload.
   - `mock_close_request_performer`: Says "Goodbye" to your pretend request.

3. **TypeDispatcher**: Think of it as a talent agent, matching intents to the right performer. (Because even mock performers need representation!)

4. **Sequence of Effects**: Like a to-do list but written in a convoluted way to impress your functional programming friends.

## Running the Show 🎬

Save it as `mock.py` and let the magic unfold:

```bash
python mock.py
Mock: Creating request...
Mock: Updating request mock-request-id with payload: {'status': 'scheduled'}
Mock: Closing request mock-request-id
Mock sequence completed successfully: {'id': 'mock-request-id', 'status': 'closed'}
```

Or as we like to call it: **a job well done, with absolutely no jobs done.**

## Why Would You Do This? 🤷‍♀️

- **Testing without Drama**: Perfect for when you want to avoid real HTTP calls but still want to feel fancy.
- **Feels Functional-ish**: Give your code that stateless, pure-function look without needing to leave the cozy embrace of Python.
- **Make Your Friends Question Your Life Choices**: Show them your new hobby of turning Python into Haskell, and watch their admiration (or concern) grow.

## When Should You Avoid This? 🚫

- When you just want a simple script. Seriously, don’t do this to yourself.
- When you have deadlines. This might delay them... by a lot.
- When you’re allergic to words like "monad" or "dispatcher."

## License

This code is provided under the **MIT License** because, just like this approach, it’s pretty chill.
