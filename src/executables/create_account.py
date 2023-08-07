import argparse
import os
import random
import string

import dotenv
import faker

from account_creator import AccountCreator
from config import PROJECT_NAME
from util import log


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
        required=os.environ.get("GMAIL_BACKUP_EMAIL"),
    )
    parser.add_argument(
        "--password",
        type=str,
        help="Password to login with",
        default=generate_random_string(10),
    )
    parser.add_argument(
        "--first-name",
        type=str,
        help="First name to register with",
        default=faker.Faker().first_name(),
    )
    parser.add_argument(
        "--last-name",
        type=str,
        help="Last name to register with",
        default=faker.Faker().last_name(),
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

    return parser.parse_args()


def run_loop(args: argparse.Namespace) -> None:
    creator = AccountCreator(
        args.email, args.backup_email, args.password, args.first_name, args.last_name
    )

    creator.init()
    creator.start_new_account()

    if args.manual_input:
        login_code = input("Enter email login code: ")
    else:
        login_code = email_parser.wait_for_login_code()
    creator.input_login_code(login_code)

    if args.manual_input:
        backup_login_code = input("Enter backup email login code: ")
    else:
        backup_login_code = email_parser.wait_for_login_code()
    creator.input_backup_login_code(backup_login_code)

    if args.close_on_exit:
        creator.close()


def main() -> None:
    dotenv.load_dotenv(".env")
    args = parse_args()

    main_creds = os.environ.get("GOOGLE_OATH_CREDENTIALS_FILE_MAIN")
    backup_creds = os.environ.get("GOOGLE_OATH_CREDENTIALS_FILE_BACKUP")

    if not args.manual_input and (not main_creds or not backup_creds):
        log.print_fail(
            "Missing Google Oath Credentials.\n"
            "Either use the --manual-input flag or set the "
            "GOOGLE_OATH_CREDENTIALS_FILE_MAIN and "
            "GOOGLE_OATH_CREDENTIALS_FILE_BACKUP environment variables."
        )
        exit(1)

    log.setup_log(args.log_level, args.log_dir, PROJECT_NAME)
    log.print_ok_blue("Creating new Avion Account...")

    run_loop(args)


if __name__ == "__main__":
    main()
