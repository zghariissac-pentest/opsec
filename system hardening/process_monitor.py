#!/usr/bin/env python3

"""
Process Monitor

Purpose

Collect process information and generate
a security-oriented system activity report.

Features

1 Process enumeration
2 CPU usage analysis
3 Memory usage analysis
4 Network process detection
5 Privileged process review
6 Report generation
7 JSON export

Requirements

pip install psutil

Author

OPSEC OPS CORE
"""

import psutil
import json
import datetime


class ProcessMonitor:

    def collect_processes(self):

        processes = []

        for process in psutil.process_iter(

            [
                "pid",
                "name",
                "username",
                "cpu_percent",
                "memory_percent",
                "status"
            ]

        ):

            try:

                processes.append(

                    {
                        "pid":
                        process.info["pid"],

                        "name":
                        process.info["name"],

                        "username":
                        process.info["username"],

                        "cpu_percent":
                        process.info["cpu_percent"],

                        "memory_percent":
                        round(
                            process.info[
                                "memory_percent"
                            ],
                            2
                        ),

                        "status":
                        process.info["status"]
                    }

                )

            except (
                psutil.NoSuchProcess,
                psutil.AccessDenied
            ):

                continue

        return processes

    def top_cpu_processes(
        self,
        processes,
        limit=10
    ):

        return sorted(

            processes,

            key=lambda x:
            x["cpu_percent"],

            reverse=True

        )[:limit]

    def top_memory_processes(
        self,
        processes,
        limit=10
    ):

        return sorted(

            processes,

            key=lambda x:
            x["memory_percent"],

            reverse=True

        )[:limit]

    def privileged_processes(
        self,
        processes
    ):

        privileged = []

        for process in processes:

            user = process.get(
                "username",
                ""
            )

            if user in [

                "root",
                "administrator"

            ]:

                privileged.append(
                    process
                )

        return privileged

    def network_processes(self):

        result = []

        try:

            connections = psutil.net_connections()

            for connection in connections:

                if connection.pid:

                    result.append(

                        {
                            "pid":
                            connection.pid,

                            "status":
                            connection.status
                        }

                    )

        except Exception:

            pass

        return result

    def observations(
        self,
        processes,
        privileged
    ):

        notes = []

        notes.append(
            f"Processes observed: {len(processes)}"
        )

        notes.append(
            f"Privileged processes: {len(privileged)}"
        )

        if len(processes) > 300:

            notes.append(
                "Large process count detected."
            )

        if len(privileged) > 50:

            notes.append(
                "High number of privileged processes."
            )

        notes.append(
            "Review unexpected resource usage."
        )

        return notes

    def create_report(self):

        processes = self.collect_processes()

        privileged = (
            self.privileged_processes(
                processes
            )
        )

        report = {

            "timestamp":
            datetime.datetime.utcnow()
            .isoformat(),

            "process_count":
            len(processes),

            "top_cpu":
            self.top_cpu_processes(
                processes
            ),

            "top_memory":
            self.top_memory_processes(
                processes
            ),

            "privileged_processes":
            privileged,

            "network_processes":
            self.network_processes(),

            "observations":
            self.observations(
                processes,
                privileged
            )
        }

        return report

    def save_report(
        self,
        report,
        filename="process_report.json"
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
    print("Process Monitor")
    print("OPSEC OPS CORE")
    print("=" * 60)


def main():

    banner()

    monitor = ProcessMonitor()

    report = monitor.create_report()

    print(
        json.dumps(
            report,
            indent=4
        )
    )

    monitor.save_report(report)

    print(
        "\nReport saved to process_report.json"
    )


if __name__ == "__main__":
    main()
