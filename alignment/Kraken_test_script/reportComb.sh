FILES=/home/unhTW/share/mcbs913_2019/align_group/kraken_output/comb_output/*
for f in $FILES*.kraken
do
	fileWithPath="${f%.*}"
	name="${fileWithPath##*/}"
	./kraken-mpa-report --db database $f > ../kraken_report/mpa/$name
	# kraken-mpa-report: ./kraken-mpa-report --db database $f > ../kraken_report/mpa/$name
	# kraken-report: ./kraken-report --db database $f > ../kraken_report/$name
done