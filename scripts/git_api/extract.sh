#!/bin/bash

terms=$3
where=$2
file=$1
startc=$4
username=$5
hash=$6

if [ $# -lt 6 ]; then
	echo "Please, set up all the parameters:"
	echo "./extract.sh filename where_to_look terms start_result_index username hash"
	exit 0
fi

echo $terms
count=0
i=$startc
ii=1
dir="./data/"$file"/"$where
if [ ! -d $dir ]; then
	mkdir -p $dir
fi
date='<2015-01-01'

### Before 2015
while [ $count -le 49 ]; do
	curl -u $username:$hash "https://api.github.com/search/repositories?q=$terms+in:$where+created:$date&per_page=100&page=$ii" -o $dir"/"$file"-"$i".json"
	count=$((count+100))
	i=$((i+1))
	ii=$((ii+1))
done

### Search by Month
year=2015
months=(01 02 03 04 05 06 07 08 09 10 11 12)
day=30
while [ $year -lt 2021 ]; do
	for month in ${months[*]}; do
		echo $month"/"$year
		if [ $month -eq 02 ]; then
			day=28
		else
			if [ $month -lt 8 ]; then
				if [ $((month%2)) -eq 0 ]; then
					day=30
				else
					day=31
				fi
			else
				if [ $month -eq 08 ] || [ $month -eq 10 ] || [ $month -eq 12 ]; then
					day=31
				else
					day=30
				fi
			fi
		fi
		date=$year"-"$month"-01"..$year"-"$month"-15"
		ii=1
		while [ $count -lt 800 ]; do
			curl -u $username:$hash "https://api.github.com/search/repositories?q=$terms+in:$where+created:$date&per_page=100&page=$ii" -o $dir"/"$file"-"$i".json"
			count=$((count+100))
			i=$((i+1))
			ii=$((ii+1))
		done
		count=0
		date=$year"-"$month"-16"..$year"-"$month"-"$day
		ii=1
		while [ $count -lt 800 ]; do
			curl -u $username:$hash "https://api.github.com/search/repositories?q=$terms+in:$where+created:$date&per_page=100&page=$ii" -o $dir"/"$file"-"$i".json"
			count=$((count+100))
			i=$((i+1))
			ii=$((ii+1))
		done
		count=0
	done
	year=$((year+1))
done
###
