FILES=/home/unhTW/share/mcbs913_2019/align_group/kraken_output/*
# counter=0
for f in $FILES*.kraken
do
	fileWithPath="${f%.*}"
	name="${fileWithPath##*/}"
	./kraken-report --db database $f > ../kraken_report/$name
done
#echo "name - $f"