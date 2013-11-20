Working repo for work on aligning reads to dbg and use in error correction.

## Quickstart

```bash
git submodule init
git submodule update
cd khmer && make && cd -
cd synthetic_rand_error/ && ../make_wrapper.sh
cd ecoli_rand_error/ && ../make_wrapper.sh
```

The make_wrapper.sh script (unsurprisingly) wraps make, causing timing and memory usage stats for each target to be appended to timing.txt in the directory make was executed in.  The columns in timing.txt are make target, command, max resident size (kilobytes), wallclock time (s).  The sudo_make_wrapper.sh script will clear OS mem caches before executing each target (and as such requires root access).

TODO
Figure out why some read alignments are not marked as truncated but clearly are