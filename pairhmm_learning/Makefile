KHMER= ../khmer

KSIZE= 30
HASH_SIZE= 4e8
N_HASHES= 4

all: estimated_probabilities.txt

%.fastq.gz:
	wget ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR172/SRR172903/SRR172903.fastq.gz
	wget ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR172/SRR172902/SRR172902.fastq.gz

combined_reads.ht: SRR172902.fastq.gz SRR172903.fastq.gz
	python $(KHMER)/scripts/load-into-counting.py --ksize $(KSIZE) -x $(HASH_SIZE) -N $(N_HASHES) $@ $^

combined_reads_mapping.bam: SRR172902.fastq.gz SRR172903.fastq.gz
	bowtie2 -x ../hmp/bowtie/mock -U SRR172902.fastq.gz -U SRR172903.fastq.gz | samtools view -S -F4 -b - > combined_reads_mapping.bam

estimated_probabilities.txt: combined_reads.ht combined_reads_mapping.bam
	python learn.py combined_reads.ht combined_reads_mapping.bam > estimated_probabilities.txt
