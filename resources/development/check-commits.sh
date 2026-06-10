#!/bin/sh

MESSAGE_REGEX='(^[A-Z]{1,6}-\d{1,4}(\s\[(build|ci|docs|feat|fix|perf|refactor|style|test|i18n)(!)?\])\s-\s([A-Z]{1})(.*$))|^Merged.*|^Squashed.*|^Revert.*'
BRANCH=${BRANCH:-HEAD}
REFERENCE=${REFERENCE:-master}

get_message () {
    git log "$1" -n1 --pretty='format:%s'
}

get_author_email () {
    git log "$1" -n1 --pretty='format:%ae'
}

log=$(git log "${REFERENCE}..${BRANCH}" --pretty='format:%h')

echo "$log" | while read -r commit; do
    message=$(get_message "$commit")
    echo "$message" | grep -q -P "$MESSAGE_REGEX"
    result=$?

    if [ ! "$result" -eq 0 ]; then
        printf "Incorrect commit: '%s'\n" "$message"
        printf "Format expected '<ticket> [<tag>] - <message>'\n"
        exit 1
    fi
    author=$(get_author_email "$commit")
    echo "$author" | grep -q "@byne.com.br"
    result=$?

    if [ ! "$result" -eq 0 ]; then
        printf "Incorrect email '%s' on commit '%s'\n" "$author" "$commit"
        printf "Email expected '<user>@byne.com.br'\n"
        exit 1
    fi
done
