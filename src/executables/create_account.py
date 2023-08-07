import argparse
import os
import random
import string

import dotenv
import fake

from account_creator import AccountCreator
from config import PROJECT_NAME
from util import log


def generate_random_string(length: int) -> str:
    # Define the characters you want to include in the random string
    characters = string.ascii_letters + string.digits + string.punctuation

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

    src_dir = os.path.dirname(os.path.dirname(__file__))
    root_dir = os.path.dirname(src_dir)
    parser.add_argument(
        "--google-credentials-file",
        type=str,
        help="Google API credentials file",
        default=os.path.join(root_dir, "google_credentials.json"),
    )

    parser.add_argument(
        "--email",
        type=str,
        help="Email address to login with",
        required=True,
    )
    parser.add_argument(
        "--backup-email",
        type=str,
        help="Backup email address to register with",
        required=True,
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
        default=fake.Faker().first_name(),
    )
    parser.add_argument(
        "--last-name",
        type=str,
        help="Last name to register with",
        default=fake.Faker().last_name(),
    )

    return parser.parse_args()


def run_loop(args: argparse.Namespace) -> None:
    creator = AccountCreator(
        args.email, args.backup_email, args.password, args.first_name, args.last_name
    )

    creator.init()
    creator.start_new_account()
    # login_code = email_parser.wait_for_login_code()
    login_code = input("Enter email login code: ")
    creator.input_login_code(login_code)
    # login_code = email_parser.wait_for_login_code()
    backup_login_code = input("Enter backup email login code: ")
    creator.input_backup_login_code(backup_login_code)

    creator.close()


def main() -> None:
    args = parse_args()
    dotenv.load_dotenv(".env")

    log.setup_log(args.log_level, args.log_dir, PROJECT_NAME)
    log.print_ok_blue("Creating new Avion Account...")

    run_loop(args)


if __name__ == "__main__":
    main()
