#! /bin/zsh

if ((# < 1)); then
  echo 'Usage: dumpWork.sh <date>' >&2
  exit 1
fi

wget -q http://download.wikimedia.org/frwiki/$1/frwiki-$1-pages-articles.xml.bz2 -O - | bunzip2 > data/frwiki-$1.xml

< data/frwiki-$1.xml awk -f articlesSansPortail.awk | sort > data/articlesSansPortail-full-$1.txt
sed -n 's/ !!! music//p' data/articlesSansPortail-full-$1.txt | sort > data/articlesSansPortail-musique-$1.txt
sed -n 's/ !!! actor//p' data/articlesSansPortail-full-$1.txt | sort > data/articlesSansPortail-acteurs-$1.txt
grep -v '\!\!\! \(music\|actor\)' data/articlesSansPortail-full-$1.txt | sort > data/articlesSansPortail-$1.txt

< data/frwiki-$1.xml awk -f pagesEnImpasse.awk | sort > data/pagesEnImpasse-$1.txt

< data/frwiki-$1.xml awk -f lastEdit.awk | sort > data/lastEdit-$1.txt
