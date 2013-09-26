#!/bin/bash

function msg() {
    echo $(date +%T) "$@"
}

# Move to a predictable place.
cd $(dirname $0)

failures=0
total=0
mydir=$(pwd)
if [ -z "$1" ]; then
    styles_to_test=$(echo ../[0-9][0-9]-*)
else
    styles_to_test=../$1-*
fi

files=$(echo *.txt)

for dir in $styles_to_test ; do
    cd $dir
    for file in $files ; do
        for exe in * ; do
            if [ -x $exe ]; then
                msg testing $(basename $dir)/$exe with $file
                expected=$mydir/$file
                actual=$(./$exe ../$file)
                echo "$actual" | diff -b $expected - > /dev/null
                result=$?
                total=$((total+1))
                if [ $result -ne 0 ]; then
                    echo 
                    echo "    Expected            Actual"
                    echo "-----------------  -----------------"
                    echo "$actual" | paste $expected - | column -t
                    echo 
                    failures=$(($failures+1))
                    msg $exe FAILED!
                else
                    msg passed.
                fi
            fi
        done
    done
    cd $mydir
done

msg $(date +%T) Ran $total tests with $failures failures.
if [ $failures -ne 0 ]; then
    msg FAILED!
    exit $failures
fi
msg PASSED
