#!/bin/bash

make SHELL='echo $@: && /usr/bin/time -o timings.txt -a -f "$@\t%C\t%D\t%K\t%M\t%P\t%e" sh'