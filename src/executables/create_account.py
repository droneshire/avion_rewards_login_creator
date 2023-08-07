import argparse
import os
import random
import string

import dotenv

from account_creator import AccountCreator
from config import PROJECT_NAME
from email_parser import EmailParser
from util import log, wait


def generate_random_string(length: int) -> str:
    # Define the characters you want to include in the random string
    characters = string.ascii_letters + string.digits

    # Generate the random string
    random_string = "".join(random.choice(characters) for _ in range(length))

    return random_string[0].upper() + random_string + "!"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Property Guru Bot")

    log_dir = log.get_logging_dir(PROJECT_NAME)

    parser.add_argument("--log-dir", default=log_dir)
    parser.add_argument(
        "--log-level",
        type=str,
        help="Logging level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Run the script without actually sending SMS",
    )

    parser.add_argument(
        "--email",
        type=str,
        help="Email address to login with",
        default=os.environ.get("GMAIL_MAIN_EMAIL"),
    )
    parser.add_argument(
        "--backup-email",
        type=str,
        help="Backup email address to register with",
        default=os.environ.get("GMAIL_BACKUP_EMAIL"),
    )
    parser.add_argument(
        "--password",
        type=str,
        help="Password to login all accounts with",
        default=generate_random_string(10),
    )
    parser.add_argument(
        "--manual-input",
        action="store_true",
        help="Manually input codes instead of email parser",
    )
    parser.add_argument(
        "--close-on-exit",
        action="store_true",
        help="Close the browser on exit",
    )
    parser.add_argument(
        "--save-after-read",
        action="store_true",
        help="Save email after reading instead of deleting",
    )
    return parser.parse_args()


def get_login_code_from_parser(email: str, creds_env: str, delete_after_find: bool = False) -> str:
    creds = os.environ.get(creds_env)

    code_from_address = os.environ.get("AVION_REWARDS_EMAIL_ADDRESS")
    code_subject = os.environ.get("AVION_REWARDS_EMAIL_SUBJECT")
    code_regex = os.environ.get("AVION_REWARDS_EMAIL_REGEX")

    if not creds:
        log.print_fail(
            "Missing Google Oath Credentials.\n"
            "Either use the --manual-input flag or set the "
            "GOOGLE_OATH_CREDENTIALS_FILE_MAIN and "
            "GOOGLE_OATH_CREDENTIALS_FILE_BACKUP environment variables."
        )
        raise ValueError("Missing Google Oath Credentials.")

    if not code_from_address or not code_subject or not code_regex:
        log.print_fail(
            "Missing environment variables.\n"
            "Set AVION_REWARDS_EMAIL_ADDRESS, AVION_REWARDS_EMAIL_SUBJECT, and "
            "AVION_REWARDS_EMAIL_BODY."
        )
        raise ValueError("Missing environment variables.")

    email_parser = EmailParser(email=email, credentials_path=creds)

    login_code = email_parser.wait_for_login_code(
        from_address=code_from_address,
        subject=code_subject,
        search_regex=code_regex,
        timeout=120.0,
        delete_after_find=delete_after_find,
    )

    return login_code


def run_loop(args: argparse.Namespace) -> None:
    creator = AccountCreator(
        args.email, args.backup_email, args.password, args.first_name, args.last_name
    )

    creator.init()

    emails = [e.strip() for e in os.environ.get("ACCOUNT_EMAILS", "").split(",")]

    for email in emails:
        creator.start_new_account(email)

        wait.wait(20)

        if args.manual_input:
            login_code = input("Enter email login code: ")
        else:
            login_code = get_login_code_from_parser(
                args.email,
                "GOOGLE_OATH_CREDENTIALS_FILE_MAIN",
                delete_after_find=not args.save_after_read,
            )

        creator.input_login_code(login_code)

        if args.manual_input:
            backup_login_code = input("Enter backup email login code: ")
        else:
            backup_login_code = get_login_code_from_parser(
                args.backup_email,
                "GOOGLE_OATH_CREDENTIALS_FILE_BACKUP",
                delete_after_find=not args.save_after_read,
            )

        creator.input_backup_login_code(backup_login_code)

    if args.close_on_exit:
        creator.close()


def main() -> None:
    dotenv.load_dotenv(".env")
    args = parse_args()

    log.setup_log(args.log_level, args.log_dir, PROJECT_NAME)
    log.print_ok_blue("Creating new Avion Account...")

    run_loop(args)


if __name__ == "__main__":
    main()
