KHMER= ../khmer
DBG_NULL= ../dbg-graph-null/

GENOME_LENGTH = 1000
READ_COV = 20

KSIZE= 30
HASH_SIZE= 1e7
N_HASHES= 4

TRUSTED_CUTOFF= 3
BITS_THETA= 1
MIN_COV= 5

all: ideal_correction_details.txt read_correction_details.txt

.PHONY: all clean

genome.fasta:
	python $(DBG_NULL)/make-random-genome.py --length $(GENOME_LENGTH) > $@

reads.fasta: genome.fasta 
	python $(DBG_NULL)/make-reads.py --mutation-details mutation_details.txt --coverage $(READ_COV) $< > $@

norm_by_align.fasta.keepalign: reads.fasta
	python $(KHMER)/sandbox/normalize-by-align.py --details-out alignment_details.txt --ksize $(KSIZE) -x $(HASH_SIZE) -N $(N_HASHES) -C $(MIN_COV) -t $(TRUSTED_CUTOFF) --bits-theta $(BITS_THETA) -s norm_by_align.ht $< && mv reads.fasta.keepalign $@

read_correction_details.txt: norm_by_align.fasta.keepalign reads.fasta
	../compare.py mutation_details.txt reads.fasta norm_by_align.fasta.keepalign > read_correction_details.txt

genome.ht: genome.fasta
	python $(KHMER)/scripts/load-into-counting.py --ksize $(KSIZE) -x $(HASH_SIZE) -N $(N_HASHES) $@ $<

ideal_corrected.fasta.keepalign: genome.ht reads.fasta
	python $(KHMER)/sandbox/read_aligner.py --trusted-cov 1 --theta $(BITS_THETA) $< reads.fasta > $@ 2> ideal_alignment_details.txt

ideal_correction_details.txt: ideal_corrected.fasta.keepalign reads.fasta
	../compare.py mutation_details.txt reads.fasta ideal_corrected.fasta.keepalign > $@

clean:
	-(rm genome.fasta reads.fasta genome.ht norm_by_align.ht read_correction_details.txt alignment_details.txt mutation_details.txt norm_by_align.fasta.keepalign ideal_corrected.fasta.keepalign ideal_correction_details.txt)