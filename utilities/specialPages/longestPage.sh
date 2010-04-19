#! /bin/zsh

for page in LongPages/*; do
  echo -n "${page:s/.html//:s@LongPages/@@} "
    < $page awk '
  /^<ol/ {
    show = 1
  }

  /^<li.+\[(.+)\]<\/li>/ {
    if (show) {
      print $0
      exit
    }
  }
' $1 | sed 's/.*\[\(.*\)\].*/\1/ ; s/[^0-9]//g'
done | sort -nrk 2
