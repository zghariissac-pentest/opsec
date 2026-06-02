#!/usr/bin/env python3

"""
Clipboard Wiper

Purpose

Automatically clear clipboard contents
after a specified amount of time.

Features

1 Clipboard monitoring
2 Automatic clearing
3 Continuous mode
4 Activity logging
5 Status reporting

Requirements

pip install pyperclip

Author

OPSEC OPS CORE
"""

import pyperclip
import time
import argparse
import datetime


class ClipboardWiper:

    def __init__(self, timeout):

        self.timeout = timeout

        self.last_content = None
        self.last_change_time = None

    def get_clipboard(self):

        try:
            return pyperclip.paste()

        except Exception:
            return ""

    def clear_clipboard(self):

        try:

            pyperclip.copy("")

            return True

        except Exception:

            return False

    def log_event(self, message):

        timestamp = datetime.datetime.now()

        print(
            f"[{timestamp}] {message}"
        )

    def monitor(self):

        self.log_event(
            f"Clipboard monitoring started. Timeout: {self.timeout} seconds"
        )

        while True:

            current_content = self.get_clipboard()

            if (
                current_content
                and current_content != self.last_content
            ):

                self.last_content = current_content

                self.last_change_time = time.time()

                self.log_event(
                    "New clipboard content detected"
                )

            if (
                self.last_content
                and self.last_change_time
            ):

                elapsed = (
                    time.time()
                    - self.last_change_time
                )

                if elapsed >= self.timeout:

                    if self.clear_clipboard():

                        self.log_event(
                            "Clipboard cleared successfully"
                        )

                    else:

                        self.log_event(
                            "Failed to clear clipboard"
                        )

                    self.last_content = None
                    self.last_change_time = None

            time.sleep(1)

    def run_once(self):

        content = self.get_clipboard()

        if not content:

            print(
                "Clipboard is empty"
            )

            return

        print(
            f"Waiting {self.timeout} seconds before clearing clipboard..."
        )

        time.sleep(self.timeout)

        self.clear_clipboard()

        print(
            "Clipboard cleared"
        )


def banner():

    print("=" * 60)
    print("Clipboard Wiper")
    print("OPSEC OPS CORE")
    print("=" * 60)


def main():

    parser = argparse.ArgumentParser(
        description="Clipboard Security Tool"
    )

    parser.add_argument(
        "--timeout",
        type=int,
        default=30,
        help="Seconds before clipboard is cleared"
    )

    parser.add_argument(
        "--monitor",
        action="store_true",
        help="Continuous monitoring mode"
    )

    args = parser.parse_args()

    banner()

    wiper = ClipboardWiper(
        args.timeout
    )

    if args.monitor:

        wiper.monitor()

    else:

        wiper.run_once()


if __name__ == "__main__":
    main()
