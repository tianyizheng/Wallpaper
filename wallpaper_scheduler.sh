#!/bin/sh

usage () {
    cat <<USAGE_END
Usage:
    $0 add "/path/to/python/script"
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
        printf "*/20 * * * * `which python` `pwd`/$2 > /dev/null" >>crontab.tmp
        crontab crontab.tmp && rm -f crontab.tmp
        ;;
    *)
        usage >&2
        exit 1
        ;;
esac