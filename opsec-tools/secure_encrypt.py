#!/usr/bin/env python3

"""
Secure Encrypt

Purpose

Protect files using modern symmetric encryption.

Features

1 Generate encryption keys
2 Encrypt files
3 Decrypt files
4 Verify integrity
5 Support large files
6 Create operation reports

Requirements

pip install cryptography

Author

OPSEC OPS CORE
"""

from cryptography.fernet import Fernet
from pathlib import Path

import hashlib
import json
import datetime
import argparse


class SecureEncrypt:

    def generate_key(self, output_file="key.key"):

        """
        Generate a new encryption key.

        The key should be stored securely and separately
        from encrypted files.
        """

        key = Fernet.generate_key()

        with open(output_file, "wb") as file:
            file.write(key)

        return output_file

    def load_key(self, key_file):

        with open(key_file, "rb") as file:
            return file.read()

    def calculate_sha256(self, file_path):

        hash_object = hashlib.sha256()

        with open(file_path, "rb") as file:

            while True:

                chunk = file.read(8192)

                if not chunk:
                    break

                hash_object.update(chunk)

        return hash_object.hexdigest()

    def encrypt_file(self, file_path, key_file):

        key = self.load_key(key_file)

        cipher = Fernet(key)

        source = Path(file_path)

        output_file = source.with_suffix(
            source.suffix + ".enc"
        )

        with open(file_path, "rb") as file:
            data = file.read()

        encrypted_data = cipher.encrypt(data)

        with open(output_file, "wb") as file:
            file.write(encrypted_data)

        return str(output_file)

    def decrypt_file(self, encrypted_file, key_file):

        key = self.load_key(key_file)

        cipher = Fernet(key)

        source = Path(encrypted_file)

        output_file = source.with_suffix("")

        with open(encrypted_file, "rb") as file:
            encrypted_data = file.read()

        decrypted_data = cipher.decrypt(
            encrypted_data
        )

        with open(output_file, "wb") as file:
            file.write(decrypted_data)

        return str(output_file)

    def create_report(
        self,
        operation,
        target_file,
        result_file
    ):

        report = {
            "timestamp":
            datetime.datetime.utcnow().isoformat(),

            "operation":
            operation,

            "source_file":
            str(target_file),

            "result_file":
            str(result_file),

            "source_sha256":
            self.calculate_sha256(target_file),

            "result_sha256":
            self.calculate_sha256(result_file)
        }

        return report

    def save_report(
        self,
        report,
        output_file="operation_report.json"
    ):

        with open(output_file, "w") as file:

            json.dump(
                report,
                file,
                indent=4
            )


def banner():

    print("=" * 60)
    print("Secure Encrypt")
    print("OPSEC OPS CORE")
    print("=" * 60)


def main():

    parser = argparse.ArgumentParser(
        description="Secure File Encryption Tool"
    )

    parser.add_argument(
        "--generate-key",
        action="store_true"
    )

    parser.add_argument(
        "--encrypt"
    )

    parser.add_argument(
        "--decrypt"
    )

    parser.add_argument(
        "--key"
    )

    args = parser.parse_args()

    banner()

    tool = SecureEncrypt()

    if args.generate_key:

        key_file = tool.generate_key()

        print(
            f"\nKey generated: {key_file}\n"
        )

    elif args.encrypt and args.key:

        result = tool.encrypt_file(
            args.encrypt,
            args.key
        )

        report = tool.create_report(
            "encryption",
            args.encrypt,
            result
        )

        tool.save_report(report)

        print(
            f"\nEncrypted file created: {result}\n"
        )

    elif args.decrypt and args.key:

        result = tool.decrypt_file(
            args.decrypt,
            args.key
        )

        report = tool.create_report(
            "decryption",
            args.decrypt,
            result
        )

        tool.save_report(report)

        print(
            f"\nDecrypted file created: {result}\n"
        )

    else:

        print(
            "\nInvalid arguments provided\n"
        )


if __name__ == "__main__":
    main()
