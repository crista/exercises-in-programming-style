#!/bin/bash

function msg() {
    echo $(date +%T) "$@"
}

failures=0
total=0
mydir=$(cd $(dirname $0); pwd)
files=$(echo *.txt)
for dir in ../[0-9][0-9]-* ; do
    cd $dir
    for file in $files ; do
        exe=$(echo tf-[0-9][0-9].py)
        msg testing $(basename $dir)/$exe with $file
        python $exe ../$file | diff -b - $mydir/$file
        result=$?
        total=$((total+1))
        if [ $result -ne 0 ]; then
            failures=$(($failures+1))
            msg FAILED!
        else
            msg passed.
        fi
    done
    cd $mydir
done

msg $(date +%T) Ran $total tests with $failures failures.
if [ $failures -ne 0 ]; then
    msg FAILED!
    exit $failures
fi
msg PASSED
