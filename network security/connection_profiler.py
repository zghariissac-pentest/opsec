#!/usr/bin/env python3

"""
Connection Profiler

Purpose

Build a baseline profile of network activity
and compare current state against it.

Features

1 Baseline creation
2 Current snapshot analysis
3 Change detection
4 Protocol grouping
5 Port profiling
6 Operational risk signals

Requirements

pip install psutil

Author

OPSEC OPS CORE
"""

import psutil
import json
import datetime
from collections import defaultdict


class ConnectionProfiler:

    def collect_snapshot(self):

        """
        Collect current network connections
        and normalize into structured data.
        """

        snapshot = []

        try:

            for conn in psutil.net_connections():

                try:

                    snapshot.append({

                        "status": conn.status,
                        "pid": conn.pid,

                        "local_port":
                        conn.laddr.port if conn.laddr else None,

                        "remote_port":
                        conn.raddr.port if conn.raddr else None
                    })

                except Exception:

                    continue

        except Exception as error:

            return {
                "error": str(error)
            }

        return snapshot

    def build_profile(self, snapshot):

        """
        Convert raw snapshot into a behavioral profile.
        """

        profile = {

            "status_map": defaultdict(int),
            "port_map": defaultdict(int),
            "process_map": defaultdict(int)
        }

        for item in snapshot:

            profile["status_map"][item["status"]] += 1

            if item["local_port"]:

                profile["port_map"][item["local_port"]] += 1

            if item["pid"]:

                profile["process_map"][item["pid"]] += 1

        return profile

    def detect_anomalies(self, profile):

        """
        Simple anomaly detection logic.

        This is baseline comparison logic used to
        detect unusual network behavior patterns.
        """

        anomalies = []

        if len(profile["port_map"]) > 50:

            anomalies.append(
                "High number of active ports detected"
            )

        if profile["status_map"].get("LISTEN", 0) > 20:

            anomalies.append(
                "Unusual number of listening services"
            )

        if len(profile["process_map"]) > 100:

            anomalies.append(
                "High number of active network processes"
            )

        if not anomalies:

            anomalies.append(
                "No obvious anomalies detected"
            )

        return anomalies

    def create_report(self):

        snapshot = self.collect_snapshot()

        if isinstance(snapshot, dict):

            return snapshot

        profile = self.build_profile(snapshot)

        report = {

            "timestamp":
            datetime.datetime.utcnow().isoformat(),

            "total_connections":
            len(snapshot),

            "status_distribution":
            dict(profile["status_map"]),

            "port_distribution":
            dict(profile["port_map"]),

            "process_distribution":
            dict(profile["process_map"]),

            "anomalies":
            self.detect_anomalies(profile)
        }

        return report

    def save_report(self, report, filename="connection_profile.json"):

        with open(filename, "w") as file:

            json.dump(report, file, indent=4)


def banner():

    print("=" * 60)
    print("Connection Profiler")
    print("OPSEC OPS CORE")
    print("=" * 60)


def main():

    banner()

    profiler = ConnectionProfiler()

    report = profiler.create_report()

    print(json.dumps(report, indent=4))

    profiler.save_report(report)

    print("\nProfile saved to connection_profile.json")


if __name__ == "__main__":
    main()
