#!/bin/bash

export PYTHONPATH=`dirname $0`/khmer

make SHELL='echo 3 > /proc/sys/vm/drop_caches && echo $@: && /usr/bin/time -o timings.txt -a -f "$@\t%C\t%M\t%P\t%e" sh'