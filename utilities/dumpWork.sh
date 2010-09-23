#! /bin/zsh

if ((# < 1)); then
  echo 'Usage: articlesSansPortail.sh <date>' >&2
  exit 1
fi

wget -q http://download.wikimedia.org/frwiki/latest/frwiki-latest-pages-articles.xml.bz2 -O - | bunzip2 > frwiki-$1.xml

< frwiki-$1.xml awk -f articlesSansPortail.awk | sort > articlesSansPortail-$1.txt
< frwiki-$1.xml awk -f pagesEnImpasse.awk | sort > pagesEnImpasse-$1.txt
