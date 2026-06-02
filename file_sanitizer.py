#!/usr/bin/env python3

"""
File Sanitizer

Purpose

Analyze files before sharing or archiving.

Features

1. File information collection
2. Hash generation
3. Hidden file detection
4. Extension analysis
5. Permission inspection
6. Risk scoring
7. JSON report generation

Author

OPSEC OPS CORE
"""

import hashlib
import json
import os
import stat
from pathlib import Path
from datetime import datetime


class FileSanitizer:

    def __init__(self):

        self.risky_extensions = {
            ".exe",
            ".dll",
            ".bat",
            ".cmd",
            ".ps1",
            ".vbs",
            ".scr",
            ".jar",
            ".msi"
        }

    def get_file_information(self, file_path):

        path = Path(file_path)

        stats = path.stat()

        return {
            "name": path.name,
            "extension": path.suffix.lower(),
            "size_bytes": stats.st_size,
            "created": datetime.fromtimestamp(
                stats.st_ctime
            ).isoformat(),
            "modified": datetime.fromtimestamp(
                stats.st_mtime
            ).isoformat(),
            "absolute_path": str(path.resolve())
        }

    def calculate_hashes(self, file_path):

        md5_hash = hashlib.md5()
        sha1_hash = hashlib.sha1()
        sha256_hash = hashlib.sha256()

        with open(file_path, "rb") as file:

            while True:

                chunk = file.read(8192)

                if not chunk:
                    break

                md5_hash.update(chunk)
                sha1_hash.update(chunk)
                sha256_hash.update(chunk)

        return {
            "md5": md5_hash.hexdigest(),
            "sha1": sha1_hash.hexdigest(),
            "sha256": sha256_hash.hexdigest()
        }

    def detect_hidden_file(self, file_path):

        path = Path(file_path)

        return path.name.startswith(".")

    def analyze_extension(self, file_path):

        extension = Path(file_path).suffix.lower()

        if extension in self.risky_extensions:

            return {
                "status": "high risk",
                "reason": "executable file type"
            }

        return {
            "status": "normal",
            "reason": "non executable file type"
        }

    def inspect_permissions(self, file_path):

        permissions = stat.filemode(
            os.stat(file_path).st_mode
        )

        return permissions

    def calculate_risk_score(
        self,
        hidden,
        extension_analysis
    ):

        score = 0

        if hidden:
            score += 25

        if extension_analysis["status"] == "high risk":
            score += 50

        if score == 0:
            level = "low"

        elif score <= 50:
            level = "medium"

        else:
            level = "high"

        return {
            "score": score,
            "level": level
        }

    def analyze_file(self, file_path):

        info = self.get_file_information(
            file_path
        )

        hashes = self.calculate_hashes(
            file_path
        )

        hidden = self.detect_hidden_file(
            file_path
        )

        extension_analysis = (
            self.analyze_extension(
                file_path
            )
        )

        permissions = self.inspect_permissions(
            file_path
        )

        risk = self.calculate_risk_score(
            hidden,
            extension_analysis
        )

        report = {
            "analysis_time":
            datetime.utcnow().isoformat(),

            "file_information":
            info,

            "hashes":
            hashes,

            "hidden_file":
            hidden,

            "extension_analysis":
            extension_analysis,

            "permissions":
            permissions,

            "risk":
            risk
        }

        return report

    def save_report(
        self,
        report,
        output_file
    ):

        with open(
            output_file,
            "w",
            encoding="utf8"
        ) as file:

            json.dump(
                report,
                file,
                indent=4
            )


def banner():

    print("=" * 60)
    print("File Sanitizer")
    print("OPSEC OPS CORE")
    print("=" * 60)


def main():

    import argparse

    parser = argparse.ArgumentParser(
        description="File Sanitizer"
    )

    parser.add_argument(
        "file",
        help="Target file"
    )

    parser.add_argument(
        "--report",
        default="report.json"
    )

    args = parser.parse_args()

    banner()

    sanitizer = FileSanitizer()

    report = sanitizer.analyze_file(
        args.file
    )

    sanitizer.save_report(
        report,
        args.report
    )

    print("\nAnalysis Complete\n")

    print(
        json.dumps(
            report,
            indent=4
        )
    )


if __name__ == "__main__":
    main()
