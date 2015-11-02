#! /bin/zsh

if ((# < 1)); then
  echo 'Usage: articlesTitlesToVerify.sh <date>' >&2
  exit 1
fi

export LC_ALL=C
export LANG=C

wget -q http://download.wikimedia.org/frwiki/latest/frwiki-latest-stub-articles.xml.gz -O - | gunzip > data/frwiki-$1-stub-articles.xml

python titles.py data/frwiki-$1-stub-articles.xml | sort > data/frwiki-titles-$1-natural.txt
python titles.py data/frwiki-$1-stub-articles.xml --skip-redirects | sort > data/frwiki-titles-$1-natural-noredirect.txt
python parens.py data/frwiki-titles-$1-natural.txt > data/frwiki-titles-paren-noprefix-open-$1.txt

comm -1 -2 data/frwiki-titles-$1-natural-noredirect.txt data/frwiki-titles-paren-noprefix-open-$1.txt >| data/frwiki-titles-paren-noprefix-open-noredirect-$1.txt
