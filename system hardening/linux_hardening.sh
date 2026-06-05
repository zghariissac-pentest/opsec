#!/bin/bash

#
# Linux Hardening Audit
#
# Purpose
#
# Review system security posture and
# generate a hardening report.
#
# Author
#
# OPSEC OPS CORE
#

REPORT_FILE="hardening_report.txt"

banner() {

    echo "=================================================="
    echo "Linux Hardening Audit"
    echo "OPSEC OPS CORE"
    echo "=================================================="
    echo
}

write_report() {

    echo "$1" >> "$REPORT_FILE"
}

section() {

    echo
    echo "[ $1 ]"
    echo

    write_report ""
    write_report "[ $1 ]"
    write_report ""
}

check_updates() {

    section "System Updates"

    if command -v dnf >/dev/null 2>&1; then

        COUNT=$(dnf check-update 2>/dev/null | wc -l)

        echo "Update check completed"

        write_report "Update entries detected: $COUNT"

    elif command -v apt >/dev/null 2>&1; then

        apt list --upgradable 2>/dev/null \
        >> "$REPORT_FILE"

    else

        write_report "Package manager not detected"
    fi
}

check_firewall() {

    section "Firewall Status"

    if command -v firewall-cmd >/dev/null 2>&1; then

        STATUS=$(firewall-cmd --state 2>/dev/null)

        echo "Firewall: $STATUS"

        write_report "Firewall status: $STATUS"

    elif command -v ufw >/dev/null 2>&1; then

        STATUS=$(ufw status)

        write_report "$STATUS"

    else

        write_report "Firewall tool not detected"
    fi
}

check_services() {

    section "Enabled Services"

    systemctl list-unit-files \
    --type=service \
    --state=enabled \
    >> "$REPORT_FILE" 2>/dev/null
}

check_listening_ports() {

    section "Listening Ports"

    ss -tuln >> "$REPORT_FILE" 2>/dev/null
}

check_world_writable() {

    section "World Writable Files"

    find / \
    -xdev \
    -type f \
    -perm -002 \
    2>/dev/null \
    | head -50 \
    >> "$REPORT_FILE"
}

check_sudo_users() {

    section "Administrative Accounts"

    getent group sudo >> "$REPORT_FILE" 2>/dev/null

    getent group wheel >> "$REPORT_FILE" 2>/dev/null
}

check_kernel() {

    section "Kernel Information"

    uname -a >> "$REPORT_FILE"
}

generate_summary() {

    section "Summary"

    write_report "Review enabled services."
    write_report "Review listening ports."
    write_report "Review update status."
    write_report "Review administrative access."
    write_report "Review file permissions."
}

main() {

    banner

    rm -f "$REPORT_FILE"

    check_updates
    check_firewall
    check_services
    check_listening_ports
    check_world_writable
    check_sudo_users
    check_kernel
    generate_summary

    echo
    echo "Audit completed"
    echo
    echo "Report saved:"
    echo "$REPORT_FILE"
    echo
}

main
