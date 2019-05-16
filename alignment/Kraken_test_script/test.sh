FILES=/home/unhTW/share/mcbs913_2019/align_group/test_datasets/*
for f in $FILES*.fastq
do
	fileWithPath="${f%.*}"
	name="${fileWithPath##*/}"
	time ./kraken --preload --threads 32 --db database $f > ../kraken_output/$name.kraken
done
#echo "name - $f"