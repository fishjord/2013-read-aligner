#!/usr/bin/env python

import pysam
import khmer
import argparse

cigar_to_state = { 0 : 'M', 1 : 'Ir', 2 : 'Ig' }

def extract_cigar(cigar):
  ret = []
  for t, length in cigar:
    for i in range(length):
      ret.append(cigar_to_state[t])

  return ret

def trusted_str(cov, trusted_cutoff):
  if cov < trusted_cutoff:
    return '_u'
  else:
    return '_t'

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('--trusted-cutoff', type=int, default=5)
  parser.add_argument("ht", type=str, help="Counting bloom filter for the reads")
  parser.add_argument("bam_file", type=str, help="bam read mapping file")

  args = parser.parse_args()

  ht = khmer.load_counting_hash(args.ht)
  samfile = pysam.Samfile(args.bam_file)

  k = ht.ksize()
  seq_cnt = 0
  dropped_seqs = 0
  base_cnt = {}
  state_cnts = {}
  trans_cnts = {}

  total_bases = 0.0

  for rec in samfile:
    seq = rec.seq
    cigar = rec.cigar

    seq_cnt += 1
    if 'N' in seq:
      dropped_seqs += 1
      continue

    states = extract_cigar(cigar)
    
    kmer = seq[:k]
    state = states[k] + trusted_str(ht.count(kmer), args.trusted_cutoff)

    state_cnts[state] = state_cnts.get(state, 0) + 1
    base_cnt[kmer[-1]] = base_cnt.get(kmer[-1], 0) + 1

    for i in range(1, len(seq) - k - 1):
      total_bases += 1
      kmer = seq[i:i+k]
      cov = ht.get(kmer)

      last_state = state
      state = states[i] + trusted_str(cov, args.trusted_cutoff)

      trans = last_state + '-' + state
      trans_cnts[trans] = trans_cnts.get(trans, 0) + 1


      state_cnts[state] = state_cnts.get(state, 0) + 1
      base_cnt[kmer[-1]] = base_cnt.get(kmer[-1], 0) + 1

  print "kmer size=", k
  print "seq count=", seq_cnt, "dropped seqs=", dropped_seqs
  print "base counts=", base_cnt
  print "state counts=", state_cnts 
  print "trans counts=", trans_cnts

  for trans in sorted(trans_cnts.keys()):
    start_state = trans.split('-')[0]
    cnt = float(state_cnts[start_state])
    print '{0}\t{1:0.7f}'.format(trans, trans_cnts[trans] / cnt)

if __name__ == "__main__":
  main()
