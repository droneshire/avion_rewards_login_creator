import base64
import re
import time

from bs4 import BeautifulSoup
from bs4.element import Tag

from util import gmail, log


class EmailParser:
    def __init__(self, email: str, credentials_path: str):
        self.service = gmail.gmail_authenticate(email=email, credentials_path=credentials_path)
        self.email = email

    def wait_for_login_code(
        self,
        from_address: str,
        subject: str,
        search_regex: str,
        timeout: float = 60.0,
        delete_after_find: bool = False,
    ) -> str:
        # pylint: disable=too-many-locals
        start = time.time()

        log.print_bright("Checking for login code...")

        while True:
            if time.time() - start > timeout:
                log.print_fail_arrow("\nTimed out waiting for login code.")
                break

            messages = gmail.search_messages(self.service, f"from:{from_address} subject:{subject}")

            for message in messages:
                message_id = message["id"]
                # pylint: disable=no-member
                raw_result = (
                    self.service.users().messages().get(userId="me", id=message_id).execute()
                )

                payload = raw_result["payload"]
                headers = payload["headers"]

                for header_dict in headers:
                    if header_dict["name"] == "Subject":
                        subject = header_dict["value"]
                    if header_dict["name"] == "From":
                        sender = header_dict["value"]

                parts = payload.get("parts")[0]
                data = parts["body"]["data"]
                data = data.replace("-", "+").replace("_", "/")
                decoded_data = base64.b64decode(data)

                soup: Tag = BeautifulSoup(decoded_data, "lxml")

                if soup is None:
                    continue

                body = soup.body()  # type: ignore

                log.print_bright(f"From: {sender}")
                log.print_normal(f"Subject: {subject}")
                for line in body:
                    match = re.search(search_regex, str(line))
                    if not match:
                        continue
                    login_code = match.group(1)
                    log.print_ok(f"Login Code: {login_code}")
                    if login_code.isdigit():
                        if delete_after_find:
                            gmail.delete_messages(
                                self.service, f"from:{from_address} subject:{subject}"
                            )
                        return login_code
            log.print_normal("\rWaiting to find login code...")
            time.sleep(5.0)

        return ""
