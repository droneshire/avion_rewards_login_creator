import argparse
import os
import random
import typing as T

import dotenv
from bot import ScraperBot

from config import PROJECT_NAME
from util import log, telegram_util, wait


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

    return parser.parse_args()


def run_loop(args: argparse.Namespace) -> None:
    creator = AccountCreator()

    bot.init()

    while True:
        bot.run()
        wait.wait(args.time_between_loops)


def main() -> None:
    args = parse_args()
    dotenv.load_dotenv(".env")

    log.setup_log(args.log_level, args.log_dir, PROJECT_NAME)
    log.print_ok_blue("Starting Property Guru Bot")

    bot_pidfile = os.environ.get("BOT_PIDFILE", "monitor_inventory.pid")

    with open(bot_pidfile, "w", encoding="utf-8") as outfile:
        outfile.write(str(os.getpid()))

    try:
        run_loop(args)
    finally:
        os.remove(bot_pidfile)


if __name__ == "__main__":
    main()
