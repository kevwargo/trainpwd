#!/usr/bin/python3

import logging
import os
import random
import sys
import time
from getpass import getpass
from subprocess import CalledProcessError, check_output, run

KDIALOG_ARGS = ["kdialog", "--title", "Train Password"]


def main():
    id_ = sys.argv[1] if len(sys.argv) > 1 else "Default"

    passwd = getpass("Set up a password for training: ")
    if passwd != getpass("Repeat the password: "):
        print("Passwords don't match")
        exit(1)

    if not os.fork():
        run_training(id_, passwd)


def run_training(id_: str, passwd: str):
    log_handler = logging.FileHandler(os.path.expanduser("~/.cache/trainpwd.log"))
    log_handler.setFormatter(logging.Formatter("[%(levelname)s] %(asctime)s | %(message)s"))
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    logger.addHandler(log_handler)

    try:
        while True:
            time.sleep(random.randint(30, 60) * 60)

            while True:
                try:
                    user_passwd = kdialog_askpass(f"Provide {id_} password")
                except CalledProcessError:
                    logger.info(f"Password training for {id_} was cancelled")
                    return

                if user_passwd == passwd:
                    kdialog_ok("Correct")
                    break

                kdialog_error("Wrong!")

    except Exception as e:
        logger.exception(str(e))


def kdialog_askpass(prompt: str) -> str:
    return check_output(
        KDIALOG_ARGS + ["--password", f"{prompt}. Close the window or press Cancel to stop asking."],
        encoding="utf-8",
    ).rstrip("\n")


def kdialog_error(text: str):
    run(KDIALOG_ARGS + ["--error", text])


def kdialog_ok(text: str):
    run(KDIALOG_ARGS + ["--msgbox", text])


if __name__ == "__main__":
    main()
