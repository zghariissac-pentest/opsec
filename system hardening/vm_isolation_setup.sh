#!/bin/bash

#
# VM Isolation Assessment
#
# Purpose
#
# Evaluate whether the current system
# is suitable for isolated virtual machine use.
#
# Author
#
# OPSEC OPS CORE
#

REPORT_FILE="vm_isolation_report.txt"

banner() {

    echo "=================================================="
    echo "VM Isolation Assessment"
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

check_virtualization_support() {

    section "Processor Virtualization Support"

    if grep -E "(vmx|svm)" /proc/cpuinfo >/dev/null
    then

        echo "Virtualization support detected"

        report "Virtualization support detected"

    else

        echo "Virtualization support not detected"

        report "Virtualization support not detected"
    fi
}

check_kvm_modules() {

    section "Virtualization Modules"

    lsmod | grep kvm >> "$REPORT_FILE"

    if lsmod | grep kvm >/dev/null
    then

        echo "KVM modules available"

        report "KVM modules available"

    else

        echo "KVM modules not loaded"

        report "KVM modules not loaded"
    fi
}

check_virtualization_tools() {

    section "Virtualization Software"

    tools=(
        qemu-system-x86_64
        virt-manager
        virsh
        VBoxManage
    )

    for tool in "${tools[@]}"
    do

        if command -v "$tool" >/dev/null 2>&1
        then

            report "$tool detected"

        else

            report "$tool not detected"

        fi

    done
}

check_network_bridges() {

    section "Network Bridges"

    ip link show | grep bridge >> "$REPORT_FILE"
}

check_virtual_networks() {

    section "Virtual Networks"

    if command -v virsh >/dev/null 2>&1
    then

        virsh net-list --all \
        >> "$REPORT_FILE" \
        2>/dev/null
    fi
}

check_storage_locations() {

    section "Virtual Machine Storage"

    common_paths=(
        "$HOME/VirtualBox VMs"
        "/var/lib/libvirt/images"
        "$HOME/vms"
    )

    for path in "${common_paths[@]}"
    do

        if [ -d "$path" ]
        then

            report "Detected: $path"
        fi
    done
}

check_memory() {

    section "System Memory"

    free -h >> "$REPORT_FILE"
}

check_cpu() {

    section "Processor Information"

    lscpu >> "$REPORT_FILE"
}

recommendations() {

    section "Isolation Recommendations"

    report "Separate personal and research environments."
    report "Use dedicated virtual machines per activity."
    report "Avoid account crossover between environments."
    report "Use snapshots before major changes."
    report "Review network configuration regularly."
    report "Avoid sharing folders between isolated contexts."
}

main() {

    banner

    rm -f "$REPORT_FILE"

    check_virtualization_support
    check_kvm_modules
    check_virtualization_tools
    check_network_bridges
    check_virtual_networks
    check_storage_locations
    check_memory
    check_cpu
    recommendations

    echo
    echo "Assessment completed"
    echo
    echo "Report saved:"
    echo "$REPORT_FILE"
    echo
}

main
