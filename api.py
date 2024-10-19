# Define intents (representing each HTTP action)
class CreateRequest:
    def __init__(self, payload):
        self.payload = payload

class UpdateRequest:
    def __init__(self, request_id, payload):
        self.request_id = request_id
        self.payload = payload

class CloseRequest:
    def __init__(self, request_id):
        self.request_id = request_id
