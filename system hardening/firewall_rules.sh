#!/bin/bash

#
# Firewall Rules Assessment
#
# Purpose
#
# Inspect firewall configuration and
# generate a security report.
#
# Author
#
# OPSEC OPS CORE
#

REPORT_FILE="firewall_report.txt"

banner() {

    echo "=================================================="
    echo "Firewall Rules Assessment"
    echo "OPSEC OPS CORE"
    echo "=================================================="
    echo
}

report() {

    echo "$1" >> "$REPORT_FILE"
}

section() {

    echo
    echo "[ $1 ]"
    echo

    report ""
    report "[ $1 ]"
    report ""
}

check_firewalld() {

    section "Firewalld Status"

    if command -v firewall-cmd >/dev/null 2>&1
    then

        STATUS=$(firewall-cmd --state 2>/dev/null)

        report "Status: $STATUS"

        firewall-cmd --list-all \
        >> "$REPORT_FILE" \
        2>/dev/null

    else

        report "Firewalld not installed"
    fi
}

check_ufw() {

    section "UFW Status"

    if command -v ufw >/dev/null 2>&1
    then

        ufw status verbose \
        >> "$REPORT_FILE" \
        2>/dev/null

    else

        report "UFW not installed"
    fi
}

check_iptables() {

    section "IPTables Rules"

    if command -v iptables >/dev/null 2>&1
    then

        iptables -L -n -v \
        >> "$REPORT_FILE" \
        2>/dev/null

    else

        report "IPTables not available"
    fi
}

check_nftables() {

    section "NFTables Rules"

    if command -v nft >/dev/null 2>&1
    then

        nft list ruleset \
        >> "$REPORT_FILE" \
        2>/dev/null

    else

        report "NFTables not available"
    fi
}

check_listening_services() {

    section "Listening Services"

    ss -tuln >> "$REPORT_FILE"
}

check_open_ports() {

    section "Open Ports"

    ss -tulpn >> "$REPORT_FILE"
}

check_default_policies() {

    section "Default Policies"

    if command -v iptables >/dev/null 2>&1
    then

        iptables -L \
        >> "$REPORT_FILE" \
        2>/dev/null
    fi
}

generate_recommendations() {

    section "Recommendations"

    report "Review exposed services."
    report "Remove unnecessary listening ports."
    report "Restrict unused inbound access."
    report "Verify default policies."
    report "Review temporary rules regularly."
    report "Document intentional exceptions."
}

main() {

    banner

    rm -f "$REPORT_FILE"

    check_firewalld
    check_ufw
    check_iptables
    check_nftables
    check_listening_services
    check_open_ports
    check_default_policies
    generate_recommendations

    echo
    echo "Firewall assessment completed"
    echo
    echo "Report saved:"
    echo "$REPORT_FILE"
    echo
}

main
