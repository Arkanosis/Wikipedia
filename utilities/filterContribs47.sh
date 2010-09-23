#! /usr/bin/zsh

< lastMonthContribs_*.txt(om[1]) | grep '^41\.104\..*' | cut -d ' ' -f 1 | sort | uniq -c | sort -nr | sed 's@^[	 ]*\([0-9]\+\)[ 	]\+\([^ ]*\)$@* [[Spécial:Contributions/\2|\2]] — \1@'
