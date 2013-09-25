#!/bin/sh

grep -o "[A-Za-z][A-Za-z][A-Za-z]*" $1 \
    | tr '[:upper:]' '[:lower:]' \
    | grep -Ev "^($(sed  -e 's/,/|/g' ../stop_words.txt))$" \
    | sort | uniq -c | sort -rn | head -25 \
    | sed -e 's/^ *\([0-9]*\) *\([a-z]*\)/\2  -  \1/'
