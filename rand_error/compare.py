#!/usr/bin/python

import sys
import screed

if len(sys.argv) != 4:
    print >>sys.stderr, "USAGE: compare.py <mutations.txt> <orig.fasta> <corrected.fasta>"
    sys.exit(1)

mutations = {}
orig_reads = {}

for line in open(sys.argv[1]):
    lexemes = line.strip().split("\t")
    if len(lexemes) != 4:
        continue

    read_name = lexemes[0]
    pos = int(lexemes[1])

    if read_name not in mutations:
        mutations[read_name] = {}
    mutations[read_name][pos] = (lexemes[2], lexemes[3])

for n, record in enumerate(screed.open(sys.argv[2])):
    orig_reads[record["name"]] = record["sequence"]

print "read\ttp\tfp\ttn\tfn\ttotal_errors"
for n, record in enumerate(screed.open(sys.argv[3])):
    name = record["name"]
    seq = record["sequence"]
    orig = orig_reads[name]

    read_mut = mutations.get(name, {})
    tp, fp, tn, fn = 0, 0, 0, 0

    for pos in range(len(seq)):
        if pos >= len(orig):
            print >>sys.stderr, "{0}\n{1}\n{2}".format(name, seq, orig)
        if pos in read_mut:
            if seq[pos] == read_mut[pos][1]:
                tp += 1
            else:
                fn += 1
        else:
            if seq[pos] == orig[pos]:
                tn += 1
            else:
                fp += 1

    print "{0}\t{1}\t{2}\t{3}\t{4}\t{5}".format(name, tp, fp, tn, fn, len(read_mut))
