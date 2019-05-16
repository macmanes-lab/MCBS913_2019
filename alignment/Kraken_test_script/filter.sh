FILES=/home/unhTW/share/mcbs913_2019/align_group/kraken_output/comb_output/*
for f in $FILES*.kraken
do
	fileWithPath="${f%.*}"
	name="${fileWithPath##*/}"
	./kraken-filter --db database $f > ../kraken_report/confidence/$name%%Confidence
done
# [--threshold NUM]