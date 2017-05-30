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
noportal=`wc -l data/articlesSansPortail-$1.txt | cut -d ' ' -f 1`
echo Articles sans portail: $noportal \($(((noportal+494)/495)) pages\)
nobox=`wc -l data/articlesSansInfobox-$1.txt | cut -d ' ' -f 1`
echo Articles sans infobox: $nobox \($(((nobox+494)/495)) pages\)

python dumpwork.py $debug -dump $dump $1
