#!/usr/bin/env python3

"""
Metadata Scrubber

Features

1. Display image metadata
2. Export metadata report
3. Create metadata free copy
4. Preserve image quality
5. Process single file or directory

Supported Formats

JPEG
JPG
PNG
WEBP

Author
OPSEC OPS CORE
"""

from pathlib import Path
from PIL import Image
from PIL.ExifTags import TAGS
import json
import argparse
import datetime


class MetadataScrubber:

    def __init__(self):
        self.supported_formats = {
            ".jpg",
            ".jpeg",
            ".png",
            ".webp"
        }

    def extract_metadata(self, image_path):
        """
        Extract metadata from image.
        """

        metadata = {}

        try:
            image = Image.open(image_path)

            exif = image.getexif()

            if not exif:
                return metadata

            for tag_id, value in exif.items():

                tag_name = TAGS.get(tag_id, str(tag_id))

                try:
                    metadata[tag_name] = str(value)
                except Exception:
                    metadata[tag_name] = "unable to parse"

        except Exception as error:
            metadata["error"] = str(error)

        return metadata

    def generate_report(self, image_path):

        report = {
            "file": str(image_path),
            "scan_time": str(datetime.datetime.utcnow()),
            "metadata": self.extract_metadata(image_path)
        }

        return report

    def save_report(self, report, output_file):

        with open(output_file, "w", encoding="utf8") as file:
            json.dump(report, file, indent=4)

    def create_clean_copy(self, source_path, destination_path):
        """
        Rebuild image from pixel data only.

        This removes embedded metadata while preserving
        visual content.
        """

        image = Image.open(source_path)

        pixel_data = list(image.getdata())

        clean_image = Image.new(
            image.mode,
            image.size
        )

        clean_image.putdata(pixel_data)

        clean_image.save(destination_path)

    def process_file(self, image_path, output_directory):

        image_path = Path(image_path)
        output_directory = Path(output_directory)

        output_directory.mkdir(
            parents=True,
            exist_ok=True
        )

        clean_name = (
            image_path.stem +
            "_clean" +
            image_path.suffix
        )

        report_name = (
            image_path.stem +
            "_report.json"
        )

        clean_output = output_directory / clean_name
        report_output = output_directory / report_name

        report = self.generate_report(image_path)

        self.save_report(
            report,
            report_output
        )

        self.create_clean_copy(
            image_path,
            clean_output
        )

        return {
            "original": str(image_path),
            "clean_copy": str(clean_output),
            "report": str(report_output)
        }

    def process_directory(self, directory, output_directory):

        results = []

        directory = Path(directory)

        for file in directory.iterdir():

            if file.suffix.lower() not in self.supported_formats:
                continue

            try:
                result = self.process_file(
                    file,
                    output_directory
                )

                results.append(result)

            except Exception as error:

                results.append({
                    "file": str(file),
                    "error": str(error)
                })

        return results


def banner():

    print("=" * 60)
    print("Metadata Scrubber")
    print("OPSEC OPS CORE")
    print("=" * 60)


def main():

    parser = argparse.ArgumentParser(
        description="Image Metadata Scrubber"
    )

    parser.add_argument(
        "--file",
        help="Single image file"
    )

    parser.add_argument(
        "--directory",
        help="Directory of images"
    )

    parser.add_argument(
        "--output",
        default="output",
        help="Output directory"
    )

    args = parser.parse_args()

    banner()

    scrubber = MetadataScrubber()

    if args.file:

        result = scrubber.process_file(
            args.file,
            args.output
        )

        print("\nCompleted\n")
        print(json.dumps(result, indent=4))

    elif args.directory:

        results = scrubber.process_directory(
            args.directory,
            args.output
        )

        print("\nCompleted\n")
        print(json.dumps(results, indent=4))

    else:

        print(
            "\nProvide either --file or --directory\n"
        )


if __name__ == "__main__":
    main()
