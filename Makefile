KHMER= ../khmer
DBG_NULL= dbg-graph-null/

KSIZE= 30
HASH_SIZE= 1e7
N_HASHES= 4

all: test.ht

test_genome.fasta:
	python $(DBG_NULL)/make-random-genome-with-repeats.py > $@

test_reads.fasta: test_genome.fasta 
	python $(DBG_NULL)/make-reads.py $< > $@

test.ht: test_reads.fasta
	$(KHMER)/scripts/load-into-counting.py --ksize $(KSIZE) -x $(HASH_SIZE) --n_hashes $(N_HASHES) $@ $<