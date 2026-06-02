#!/usr/bin/env python3

"""
DNS Leak Tester

Purpose

Inspect DNS configuration and generate
a report describing resolver information.

Features

1 DNS configuration discovery
2 Resolver testing
3 Response timing
4 Report generation
5 Operational observations
6 JSON export

Author

OPSEC OPS CORE
"""

import socket
import json
import time
import platform
import subprocess
import datetime


class DNSLeakTester:

    def __init__(self):

        self.test_domains = [
            "google.com",
            "cloudflare.com",
            "github.com",
            "wikipedia.org"
        ]

    def get_system_dns(self):

        """
        Attempt to discover configured
        DNS servers from the operating system.
        """

        dns_servers = []

        try:

            if platform.system() == "Linux":

                with open("/etc/resolv.conf") as file:

                    for line in file:

                        if line.startswith("nameserver"):

                            dns_servers.append(
                                line.split()[1]
                            )

        except Exception as error:

            dns_servers.append(
                f"error: {error}"
            )

        return dns_servers

    def resolve_domain(self, domain):

        """
        Resolve a domain and record timing.
        """

        result = {
            "domain": domain
        }

        try:

            start = time.time()

            ip = socket.gethostbyname(domain)

            end = time.time()

            result["ip"] = ip

            result["resolution_time_ms"] = round(
                (end - start) * 1000,
                2
            )

            result["status"] = "success"

        except Exception as error:

            result["status"] = "failed"

            result["error"] = str(error)

        return result

    def run_resolution_tests(self):

        results = []

        for domain in self.test_domains:

            results.append(
                self.resolve_domain(domain)
            )

        return results

    def generate_observations(
        self,
        dns_servers
    ):

        observations = []

        if len(dns_servers) == 0:

            observations.append(
                "No DNS servers detected."
            )

        if len(dns_servers) == 1:

            observations.append(
                "Single resolver configuration detected."
            )

        if len(dns_servers) > 1:

            observations.append(
                "Multiple resolvers configured."
            )

        observations.append(
            "Review resolver ownership and trust."
        )

        return observations

    def build_report(self):

        dns_servers = self.get_system_dns()

        resolution_results = (
            self.run_resolution_tests()
        )

        report = {

            "timestamp":
            datetime.datetime.utcnow().isoformat(),

            "dns_servers":
            dns_servers,

            "resolution_tests":
            resolution_results,

            "observations":
            self.generate_observations(
                dns_servers
            )
        }

        return report

    def save_report(
        self,
        report,
        filename="dns_report.json"
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
    print("DNS Leak Tester")
    print("OPSEC OPS CORE")
    print("=" * 60)


def main():

    banner()

    tester = DNSLeakTester()

    report = tester.build_report()

    print(
        json.dumps(
            report,
            indent=4
        )
    )

    tester.save_report(report)

    print(
        "\nReport saved to dns_report.json"
    )


if __name__ == "__main__":
    main()
