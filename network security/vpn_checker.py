#!/usr/bin/env python3

"""
VPN Checker

Purpose

Collect network information and help identify
whether the current connection matches the
expected operational profile.

Features

1 Public IP discovery
2 ASN information
3 Organization detection
4 Country detection
5 JSON reporting
6 Operational observations

Requirements

pip install requests

Author

OPSEC OPS CORE
"""

import requests
import json
import datetime
from pathlib import Path


class VPNChecker:

    def __init__(self):

        self.ip_service = "https://api.ipify.org?format=json"

        self.geo_service = (
            "https://ipinfo.io/{ip}/json"
        )

    def get_public_ip(self):

        """
        Obtain current public IP address.
        """

        try:

            response = requests.get(
                self.ip_service,
                timeout=10
            )

            response.raise_for_status()

            data = response.json()

            return data.get("ip")

        except Exception as error:

            return {
                "error": str(error)
            }

    def get_network_profile(self, ip):

        """
        Collect network information associated
        with the public IP address.
        """

        try:

            response = requests.get(
                self.geo_service.format(ip=ip),
                timeout=10
            )

            response.raise_for_status()

            data = response.json()

            return {
                "ip": ip,
                "hostname": data.get("hostname"),
                "city": data.get("city"),
                "region": data.get("region"),
                "country": data.get("country"),
                "organization": data.get("org"),
                "postal_code": data.get("postal"),
                "timezone": data.get("timezone")
            }

        except Exception as error:

            return {
                "error": str(error)
            }

    def generate_observations(self, profile):

        """
        Generate simple observations.

        These observations are informational
        and help highlight what information
        is visible externally.
        """

        observations = []

        if profile.get("organization"):
            observations.append(
                "Network provider information is visible."
            )

        if profile.get("country"):
            observations.append(
                "Geographic information is available."
            )

        if profile.get("hostname"):
            observations.append(
                "Hostname information is exposed."
            )

        if len(observations) == 0:

            observations.append(
                "Limited profile information available."
            )

        return observations

    def build_report(self):

        ip = self.get_public_ip()

        if isinstance(ip, dict):

            return ip

        profile = self.get_network_profile(ip)

        report = {
            "timestamp":
            datetime.datetime.utcnow().isoformat(),

            "network_profile":
            profile,

            "observations":
            self.generate_observations(profile)
        }

        return report

    def save_report(
        self,
        report,
        filename="vpn_report.json"
    ):

        with open(
            filename,
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
    print("VPN Checker")
    print("OPSEC OPS CORE")
    print("=" * 60)


def main():

    banner()

    checker = VPNChecker()

    report = checker.build_report()

    print(
        json.dumps(
            report,
            indent=4
        )
    )

    checker.save_report(report)

    print(
        "\nReport saved to vpn_report.json"
    )


if __name__ == "__main__":
    main()
