from util import gmail, log


class EmailParser:
    def __init__(self, email: str, credentials_path: str):
        self.service = gmail.get_service(email, password)
