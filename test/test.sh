#!/bin/bash

function msg() {
    echo "$@"
}

function date_diff() {
	date -u -d @"$(($2 - $1))" +"%-Hh %-Mm %-Ss"
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
suite_start=$(date +"%s")
for dir in $styles_to_test ; do
    cd $dir
    for file in $files ; do
        for exe in * ; do
            if [ -x $exe ]; then
                msg $(date +%T) testing $(basename $dir)/$exe with $file
                expected=$mydir/$file
				test_start=$(date +"%s")
				if [ -e $dir/autorun ] ; then
					actual=$(./$exe <autorun | grep \# | awk '{print $2,$3,$4}')
				else
                	actual=$(./$exe ../$file | grep -)
				fi
				test_end=$(date +"%s")
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
                    msg $exe FAILED in $(date_diff $test_start $test_end)!
                else
                    msg $exe passed in $(date_diff $test_start $test_end).
                fi
            fi
        done
    done
    cd $mydir
done
suite_end=$(date +"%s")

msg Ran $total tests with $failures failures in $(date_diff $suite_start $suite_end).
if [ $failures -ne 0 ]; then
    msg FAILED!
    exit $failures
fi
msg PASSED
