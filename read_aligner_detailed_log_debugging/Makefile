all: oom_details.txt

ideal_alignment_details.txt:
	python ../../khmer/sandbox/read_aligner.py --trusted-cov 1 --theta 1 ../genome.ht test.fasta > ideal_corrected.fasta.keepalign 2> ideal_alignment_details.txt

oom_details.txt: ideal_alignment_details.txt
	grep '^curr:' ideal_alignment_details.txt | sed -r 's/[ ]+/ /g' | cut -d' ' -f2-5,7- > oom_details.txt
