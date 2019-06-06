n=1%
num_iter=3
cur_iter=0
r=1000

while [ $cur_iter -lt $num_iter ]; do
		let cur_iter+=1
		f_name=results_${r}_${cur_iter}.csv
		of_name=results_${r}_${cur_iter}.txt
		echo $r 443 $n $f_name
		sudo zmap -r $r -p 443 -n $n -o $f_name 2>&1 | tee $of_name
done