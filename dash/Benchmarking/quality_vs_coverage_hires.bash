# Program for initial testing of bindash and dashing
# Checks simulated reads vs reference genome
# Varies coverage from 1 to 50 by 1 and quality from -20 to 30 by 2

# Reference genome here
genomeA="C_coli.fna.gz"

mkdir -p "${genomeA}_dir"
cd "${genomeA}_dir"
bindash sketch --outfname=${genomeA}.sketch ../${genomeA}

# Simulate reads
# Varying coverage
for coverage in $(seq 1 1 50)
	do
	# Varying quality
	for quality in $(seq -20 2 30)
		do
		art_illumina -ss HS25 -i ../${genomeA} -l 150 -f $coverage -qs $quality -o ${coverage}_${quality}
	done
done

# This part is for bindash
# Make bindash sketches and compute distances
for coverage in $(seq 1 1 50)
	do
	for quality in $(seq -20 2 30)
		do
		# Changed to fastq
		bindash sketch --nthreads=20 --outfname=${coverage}_${quality}.sketch ${coverage}_${quality}.fq
		bindash dist --nthreads=20 ${coverage}_${quality}.sketch ${genomeA}.sketch >> bindash_results.txt
	done
done
# The distances are all in bindash_results.txt

# This part is for dashing
# Adds reference genome
echo "../${genomeA}" >> genome_paths.txt
# Adds previously made simulated reads to the genome_paths.txt list
for coverage in $(seq 1 1 50)
	do
	for quality in $(seq -20 2 30) 
		do
		echo ${coverage}_${quality}.fq >> genome_paths.txt
	done
done
# Compute for distance matrix, output in dashing_distance_matrix.txt
dashing dist -k31 -p13 -Odashing_distance_matrix.txt -osize_estimates.txt -F genome_paths.txt