class ServiceException(Exception):
    def __init__(self, message, status_code):
        self.message = message
        self.status_code = status_code
        self.json_message = message if isinstance(message, dict) else {"message": message}