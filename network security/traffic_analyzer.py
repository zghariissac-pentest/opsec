#!/usr/bin/env python3

"""
Traffic Analyzer

Purpose

Collect information about active network
connections and generate a traffic summary.

Features

1 Active connection analysis
2 Listening service detection
3 Protocol statistics
4 Connection counting
5 Report generation
6 Operational observations

Requirements

pip install psutil

Author

OPSEC OPS CORE
"""

import psutil
import json
import socket
import datetime


class TrafficAnalyzer:

    def get_connections(self):

        """
        Collect active network connections.
        """

        connections_data = []

        try:

            connections = psutil.net_connections()

            for connection in connections:

                try:

                    local_address = None
                    remote_address = None

                    if connection.laddr:

                        local_address = (
                            f"{connection.laddr.ip}:"
                            f"{connection.laddr.port}"
                        )

                    if connection.raddr:

                        remote_address = (
                            f"{connection.raddr.ip}:"
                            f"{connection.raddr.port}"
                        )

                    connections_data.append({

                        "family":
                        str(connection.family),

                        "type":
                        str(connection.type),

                        "status":
                        connection.status,

                        "local_address":
                        local_address,

                        "remote_address":
                        remote_address,

                        "process_id":
                        connection.pid
                    })

                except Exception:

                    continue

        except Exception as error:

            return {
                "error": str(error)
            }

        return connections_data

    def count_statuses(
        self,
        connections
    ):

        statistics = {}

        for connection in connections:

            status = connection.get(
                "status",
                "UNKNOWN"
            )

            statistics[status] = (
                statistics.get(status, 0) + 1
            )

        return statistics

    def identify_listening_services(
        self,
        connections
    ):

        listening = []

        for connection in connections:

            if (
                connection.get("status")
                == "LISTEN"
            ):

                listening.append(
                    connection.get(
                        "local_address"
                    )
                )

        return listening

    def generate_observations(
        self,
        connections,
        listening
    ):

        observations = []

        observations.append(
            f"Total connections observed: {len(connections)}"
        )

        observations.append(
            f"Listening services observed: {len(listening)}"
        )

        if len(listening) > 10:

            observations.append(
                "Large number of listening services detected."
            )

        if len(connections) == 0:

            observations.append(
                "No active connections detected."
            )

        observations.append(
            "Review unexpected listening ports."
        )

        return observations

    def build_report(self):

        connections = self.get_connections()

        if isinstance(
            connections,
            dict
        ):

            return connections

        listening = (
            self.identify_listening_services(
                connections
            )
        )

        report = {

            "timestamp":
            datetime.datetime.utcnow().isoformat(),

            "connection_count":
            len(connections),

            "status_statistics":
            self.count_statuses(
                connections
            ),

            "listening_services":
            listening,

            "observations":
            self.generate_observations(
                connections,
                listening
            )
        }

        return report

    def save_report(
        self,
        report,
        filename="traffic_report.json"
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
    print("Traffic Analyzer")
    print("OPSEC OPS CORE")
    print("=" * 60)


def main():

    banner()

    analyzer = TrafficAnalyzer()

    report = analyzer.build_report()

    print(
        json.dumps(
            report,
            indent=4
        )
    )

    analyzer.save_report(report)

    print(
        "\nReport saved to traffic_report.json"
    )


if __name__ == "__main__":
    main()
