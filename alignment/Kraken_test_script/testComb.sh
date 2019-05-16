FILES=/home/unhTW/share/mcbs913_2019/align_group/test_datasets/combination/*
for f in $FILES*.fastq
do
	fileWithPath="${f%.*}"
	name="${fileWithPath##*/}"
	# time ./kraken --preload --threads 32 --db database $f > ../kraken_output/comb_output/$name.kraken
	echo $name
done
# extention="${f##*.}"