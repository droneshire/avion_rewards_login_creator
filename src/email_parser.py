import time

from util import gmail, log
from util.wait import wait


class EmailParser:
    def __init__(self, email: str, credentials_path: str):
        self.service = gmail.gmail_authenticate(credentials_path)
        self.email = email

    def wait_for_login_code(
        self, from_address: str, subject: str, body: str, min_time: float = 0, timeout: float = 60.0
    ) -> str:
        login_code = ""
        start = time.time()

        while True:
            if time.time() - start > timeout:
                log.print_fail_arrow("Timed out waiting for login code.")
                break

            messages = gmail.search_messages(self.service, f"from:{from_address} subject:{subject}")

            if messages:
                message_obj = messages[0]
                message_id = message_obj["id"]
                message = (
                    self.service.users()
                    .messages()
                    .get(userId="me", id=message_id, format="full")
                    .execute()
                )
                print(message["payload"])

                login_code = message["payload"]
                if login_code.isdigit():
                    break
            wait(5)

        return login_code
