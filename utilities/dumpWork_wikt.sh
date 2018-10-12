#! /bin/zsh

if ((# < 1)); then
  echo 'Usage: dumpWork_wikt.sh <date>' >&2
  exit 1
fi

setopt MULTIOS
unset REPORTTIME

echo '[1/2] Downloading and extracting dump'
wget -q --show-progress https://dumps.wikimedia.org/frwiktionary/$1/frwiktionary-$1-pages-articles.xml.bz2 -O - | bunzip2 > data/frwiktionary-$1.xml

echo '[2/2] Processing full dump'
{ pv data/frwiktionary-$1.xml } \
    > >(./extract_synonyms.py > data/synonyms-$1.txt) \
    > >(./count_synonyms.py > data/synonyms_count-$1.txt)

echo 'Finished processing'
notify-send -u normal -t 6000 "Finished processing" -i /usr/share/icons/gnome/48x48/actions/gtk-execute.png
