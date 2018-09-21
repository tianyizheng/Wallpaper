#!/bin/sh

usage () {
    cat <<USAGE_END
Usage:
    $0 add "job-spec"
    $0 list
    $0 remove "job-spec-lineno"
USAGE_END
}

if [ -z "$1" ]; then
    usage >&2
    exit 1
fi

case "$1" in
    add)
        if [ -z "$2" ]; then
            usage >&2
            exit 1
        fi

        crontab -l >crontab.tmp
        printf '%s\n' "$2" >>crontab.tmp
        crontab crontab.tmp && rm -f crontab.tmp
        ;;
    list)
        crontab -l | cat -n
        ;;
    remove)
        if [ -z "$2" ]; then
            usage >&2
            exit 1
        fi

        crontab -l | sed -e "$2d" >crontab.tmp
        crontab crontab.tmp && rm -f crontab.tmp
        ;;
    *)
        usage >&2
        exit 1
        ;;
esac