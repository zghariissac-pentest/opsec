#!/bin/bash

#
# Secure Delete
#
# Purpose
#
# Reduce file recoverability by overwriting data
# before removing the target.
#
# Author
#
# OPSEC OPS CORE
#

LOG_FILE="secure_delete.log"

banner() {

    echo "=================================================="
    echo "Secure Delete"
    echo "OPSEC OPS CORE"
    echo "=================================================="
}

log_event() {

    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

file_info() {

    TARGET="$1"

    echo
    echo "Target Information"
    echo

    ls -lh "$TARGET" 2>/dev/null
    echo
}

secure_delete_file() {

    TARGET="$1"
    PASSES="$2"

    if [ ! -f "$TARGET" ]; then

        echo "File not found"
        log_event "File not found: $TARGET"

        return 1
    fi

    SIZE=$(stat -c%s "$TARGET" 2>/dev/null)

    echo "Deleting file..."
    echo "Size: $SIZE bytes"
    echo "Passes: $PASSES"

    log_event "Starting deletion of $TARGET"

    for ((i=1;i<=PASSES;i++))
    do

        echo "Overwrite pass $i"

        dd if=/dev/urandom \
           of="$TARGET" \
           bs=4096 \
           status=none

        sync

    done

    rm -f "$TARGET"

    if [ ! -f "$TARGET" ]; then

        echo
        echo "Deletion completed"

        log_event "Deletion completed: $TARGET"

    else

        echo
        echo "Deletion failed"

        log_event "Deletion failed: $TARGET"
    fi
}

secure_delete_directory() {

    TARGET_DIR="$1"
    PASSES="$2"

    if [ ! -d "$TARGET_DIR" ]; then

        echo "Directory not found"
        return 1
    fi

    echo
    echo "Processing directory"
    echo

    find "$TARGET_DIR" -type f | while read FILE
    do

        secure_delete_file "$FILE" "$PASSES"

    done

    rmdir "$TARGET_DIR" 2>/dev/null

    log_event "Directory processed: $TARGET_DIR"
}

confirm_action() {

    echo
    read -p "Continue? (yes/no): " ANSWER

    if [ "$ANSWER" != "yes" ]; then

        echo "Operation cancelled"
        exit 0
    fi
}

main() {

    banner

    if [ $# -lt 1 ]; then

        echo
        echo "Usage:"
        echo

        echo "./secure_delete.sh target"
        echo "./secure_delete.sh target passes"

        exit 1
    fi

    TARGET="$1"
    PASSES="${2:-3}"

    file_info "$TARGET"

    confirm_action

    if [ -f "$TARGET" ]; then

        secure_delete_file "$TARGET" "$PASSES"

    elif [ -d "$TARGET" ]; then

        secure_delete_directory "$TARGET" "$PASSES"

    else

        echo "Target does not exist"
    fi
}

main "$@"
