Working repo for work on aligning reads to dbg and use in error correction.

Quickstart:

$ git submodule init
$ git submodule update
$ cd khmer && make && cd -
$ cd rand_error && make

TODO
Figure out why some read alignments are not marked as truncated but clearly are