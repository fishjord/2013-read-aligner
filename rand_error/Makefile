KHMER= ../khmer
DBG_NULL= ../dbg-graph-null/

KSIZE= 30
HASH_SIZE= 1e7
N_HASHES= 4

TRUSTED_CUTOFF= 3
BITS_THETA= 1
MIN_COV= 5

all: reads.fasta.keepalign read_correction_details.txt

.PHONY: compare stats.ht

genome.fasta:
	python $(DBG_NULL)/make-random-genome.py > $@

reads.fasta: genome.fasta 
	python $(DBG_NULL)/make-reads.py $< > $@ 2> mutation_details.txt

random.ht: reads.fasta
	PYTHONPATH=$(KHMER)/python python $(KHMER)/sandbox/normalize-by-align.py --ksize $(KSIZE) -x $(HASH_SIZE) -N $(N_HASHES) -C $(MIN_COV) -t $(TRUSTED_CUTOFF) --bits-theta $(BITS_THETA) -s $@ $< 2> read_align_stats.txt

stats.ht: reads.fasta
	PYTHONPATH=$(KHMER)/python python normalize-by-align.py --ksize $(KSIZE) -x $(HASH_SIZE) -N $(N_HASHES) -C $(MIN_COV) -t $(TRUSTED_CUTOFF) --mutations mutation_details.txt --bits-theta $(BITS_THETA) -s $@ $<

reads.fasta.keepalign: random.ht

read_correction_details.txt: reads.fasta.keepalign reads.fasta
	./compare.py mutation_details.txt reads.fasta reads.fasta.keepalign > read_correction_details.txt