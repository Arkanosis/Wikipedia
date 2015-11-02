#! /bin/zsh

if ((# < 1)); then
  echo 'Usage: dumpWork.sh <date>' >&2
  exit 1
fi

wget -q http://dumps.wikimedia.org/frwiki/$1/frwiki-$1-pages-articles.xml.bz2 -O - | bunzip2 > data/frwiki-$1.xml

< data/frwiki-$1.xml awk -f pagesEnImpasse.awk | sort > data/pagesEnImpasse-$1.txt
< data/frwiki-$1.xml awk -f emptyPages.awk | sort > data/pagesVides-$1.txt

< data/frwiki-$1.xml awk -f lastEdit.awk | sort > data/lastEdit-$1.txt

< data/frwiki-$1.xml awk -f articlesSansPortail.awk | sort > data/articlesSansPortail-full-$1.txt
sed -n 's/ !!! music//p' data/articlesSansPortail-full-$1.txt | sort > data/articlesSansPortail-musique-$1.txt
sed -n 's/ !!! actor//p' data/articlesSansPortail-full-$1.txt | sort > data/articlesSansPortail-acteurs-$1.txt
sed -n 's/ !!! homo//p' data/articlesSansPortail-full-$1.txt | sort > data/articlesSansPortail-homo-$1.txt
grep -v '\!\!\! \(music\|actor\|homo\)' data/articlesSansPortail-full-$1.txt | sort > data/articlesSansPortail-$1.txt

< data/frwiki-$1.xml awk -f articlesSansInfobox.awk | sort > data/articlesSansInfobox-full-$1.txt
sed -n 's/ !!! music//p' data/articlesSansInfobox-full-$1.txt | sort > data/articlesSansInfobox-musique-$1.txt
sed -n 's/ !!! actor//p' data/articlesSansInfobox-full-$1.txt | sort > data/articlesSansInfobox-acteurs-$1.txt
grep -v '\!\!\! \(music\|actor\)' data/articlesSansInfobox-full-$1.txt | sort > data/articlesSansInfobox-$1.txt

#python noiw.py data/wikidatawiki-20130505.xml | sort -rn > data/articlesACreer-20130505.txt

python commercials.py data/frwiki-$1.xml | grep -v '^\(Aide\|Fichier\|MediaWiki\|Modèle\|Portail\|Projet\|Wikipédia\):' | sort > data/frwiki-commercials-$1.txt
python ns_redirects.py data/frwiki-$1.xml | sort > data/frwiki-ns_redirects-$1.txt
