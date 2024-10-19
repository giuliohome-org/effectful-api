# Define intents (representing each HTTP action)
from dataclasses import dataclass

# Define the intents using data classes
@dataclass
class CreateRequest:
    payload: dict

@dataclass
class UpdateRequest:
    request_id: str
    payload: dict

@dataclass
class CloseRequest:
    request_id: str
