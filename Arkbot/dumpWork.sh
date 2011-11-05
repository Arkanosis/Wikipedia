#! /bin/zsh

if ((# < 1)); then
  echo 'Usage: dumpWork.sh <dump>' >&2
  exit 1
fi

debug= #-debug

export LANG=fr_FR.UTF-8
dump=`date -d $1 '+%-d %B %Y'`

echo Pages en impasse: `wc -l data/pagesEnImpasse-$1.txt | cut -d ' ' -f 1`
echo Pages vides: `wc -l data/pagesVides-$1.txt | cut -d ' ' -f 1`
noportal=`wc -l data/articlesSansPortail-full-$1.txt | cut -d ' ' -f 1`
echo Articles sans portail: $noportal \($(((noportal+494)/495)) pages\)

python post.py $debug -dump $dump -mode 1 data/pagesEnImpasse-$1.txt

python post.py $debug -dump $dump -mode 2 data/pagesVides-$1.txt

python noportal.py $debug -dump $dump -mode 4 data/lastEdit-$1.txt

python noportal.py $debug -dump $dump -mode 2 data/articlesSansPortail-musique-$1.txt
python noportal.py $debug -dump $dump -mode 3 data/articlesSansPortail-acteurs-$1.txt
python noportal.py $debug -dump $dump -mode 1 data/articlesSansPortail-$1.txt
