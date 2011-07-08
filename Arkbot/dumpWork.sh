#! /bin/zsh

if ((# < 1)); then
  echo 'Usage: dumpWork.sh <dump>' >&2
  exit 1
fi

debug= #-debug
dump=`date -d $1 '+%-d %B %Y'`

python post.py $debug -dump $dump -mode 1 data/pagesEnImpasse-$1.txt
python post.py $debug -dump $dump -mode 2 data/pagesVides-$1.txt

python noportal.py $debug -dump $dump -mode 4 data/lastEdit-$1.txt

python noportal.py $debug -dump $dump -mode 2 data/articlesSansPortail-musique-$1.txt
python noportal.py $debug -dump $dump -mode 3 data/articlesSansPortail-acteurs-$1.txt
python noportal.py $debug -dump $dump -mode 1 data/articlesSansPortail-$1.txt
