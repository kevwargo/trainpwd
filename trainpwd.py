#!/usr/bin/python3

import logging
import os
import random
import sys
from getpass import getpass
from signal import SIGHUP, signal
from subprocess import CalledProcessError, check_output, run
from threading import Event

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

    wake_event = Event()

    def on_hup(sig, frame):
        logger.info(f"Sig:{sig} Frame:{frame}")
        wake_event.set()

    signal(SIGHUP, on_hup)

    try:
        while True:
            delay_minutes = random.randint(30, 60)
            logger.info(f"Will show dialog in {delay_minutes} minutes")

            if wake_event.wait(delay_minutes * 60):
                logger.info("Showing dialog on signal")
            else:
                logger.info("Showing dialog on timer")

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

            wake_event.clear()

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
