KHMER= ../khmer
DBG_NULL= ../dbg-graph-null/

GENOME_LENGTH = 100000
READ_COV = 100

KSIZE= 30
HASH_SIZE= 1e7
N_HASHES= 4

TRUSTED_CUTOFF= 5
BITS_THETA= 1
DIGINORM_COV= 20

SEQ_FILE = reads.fasta

all: ideal_correction_details.txt preload_correction_details.txt diginorm_correction_details.txt #read_correction_details.txt

.PHONY: all clean

genome.fasta:
	python $(DBG_NULL)/make-random-genome.py --length $(GENOME_LENGTH) > $@

$(SEQ_FILE): genome.fasta 
	python $(DBG_NULL)/make-reads.py --mutation-details mutation_details.txt --coverage $(READ_COV) $< > $@

norm_by_align.fasta.keepalign: $(SEQ_FILE)
	python $(KHMER)/sandbox/normalize-by-align.py --details-out alignment_details.txt --ksize $(KSIZE) -x $(HASH_SIZE) -N $(N_HASHES) -C $(DIGINORM_COV) -t $(TRUSTED_CUTOFF) --bits-theta $(BITS_THETA) -s norm_by_align.ht $< && mv $(SEQ_FILE).keepalign $@

read_correction_details.txt: norm_by_align.fasta.keepalign $(SEQ_FILE)
	../compare.py mutation_details.txt $(SEQ_FILE) norm_by_align.fasta.keepalign > read_correction_details.txt

genome.ht: genome.fasta
	python $(KHMER)/scripts/load-into-counting.py --ksize $(KSIZE) -x $(HASH_SIZE) -N $(N_HASHES) $@ $<

reads.ht: $(SEQ_FILE)
	python $(KHMER)/scripts/load-into-counting.py --ksize $(KSIZE) -x $(HASH_SIZE) -N $(N_HASHES) $@ $<

diginorm.ht: $(SEQ_FILE)
	python $(KHMER)/scripts/normalize-by-median.py --ksize $(KSIZE) -x $(HASH_SIZE) -N $(N_HASHES) -C $(DIGINORM_COV) -s $@ $<

preload_corrected.fasta.keepalign: reads.ht $(SEQ_FILE)
	python $(KHMER)/sandbox/read_aligner.py --trusted-cov $(TRUSTED_CUTOFF) --theta $(BITS_THETA) $< $(SEQ_FILE) > $@ 2> preload_alignment_details.txt

preload_correction_details.txt: preload_corrected.fasta.keepalign $(SEQ_FILE)
	../compare.py mutation_details.txt $(SEQ_FILE) $< > $@

diginorm_corrected.fasta.keepalign: diginorm.ht $(SEQ_FILE)
	python $(KHMER)/sandbox/read_aligner.py --trusted-cov $(TRUSTED_CUTOFF) --theta $(BITS_THETA) $< $(SEQ_FILE) > $@ 2> diginorm_alignment_details.txt

diginorm_correction_details.txt: diginorm_corrected.fasta.keepalign $(SEQ_FILE)
	../compare.py mutation_details.txt $(SEQ_FILE) $< > $@

ideal_corrected.fasta.keepalign: genome.ht $(SEQ_FILE)
	python $(KHMER)/sandbox/read_aligner.py --trusted-cov 1 --theta $(BITS_THETA) $< $(SEQ_FILE) > $@ 2> ideal_alignment_details.txt

ideal_correction_details.txt: ideal_corrected.fasta.keepalign $(SEQ_FILE)
	../compare.py mutation_details.txt $(SEQ_FILE) ideal_corrected.fasta.keepalign > $@

clean:
	-(rm genome.fasta $(SEQ_FILE) genome.ht* reads.ht* diginorm.ht* norm_by_align.ht* read_correction_details.txt alignment_details.txt mutation_details.txt norm_by_align.fasta.keepalign diginorm_* preload_* ideal_* $(SEQ_FILE).keep)
