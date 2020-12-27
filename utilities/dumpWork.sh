#! /bin/zsh

if ((# < 1)); then
  echo 'Usage: dumpWork.sh <date>' >&2
  exit 1
fi

setopt MULTIOS
unset REPORTTIME

echo '[1/2] Downloading, extracting and processing full dump'
wget -q --show-progress https://dumps.wikimedia.org/frwiki/$1/frwiki-$1-pages-articles.xml.bz2 -O - | bunzip2 \
    > >(awk -f pagesEnImpasse.awk | sort > data/pagesEnImpasse-$1.txt) \
    > >(awk -f emptyPages.awk | grep -vxFf emptyPages.blacklist | sort > data/pagesVides-$1.txt) \
    > >(awk -f lastEdit.awk | sort > data/lastEdit-$1.txt) \
    > >(awk -f articlesSansPortail.awk | sort > data/articlesSansPortail-full-$1.txt) \
    > >(awk -f articlesSansInfobox.awk | sort > data/articlesSansInfobox-full-$1.txt) \
    > >(python3 commercials.py | grep -v '^\(Aide\|Fichier\|MediaWiki\|Modèle\|Portail\|Projet\|Wikipédia\):' | sort > data/frwiki-commercials-$1.txt) \
    > >(python3 ns_redirects.py | sort > data/frwiki-ns_redirects-$1.txt)

echo '[2/2] Processing articles sans portail, articles sans infobox'
{ pv data/articlesSansPortail-full-$1.txt } \
    > >(sed -n 's/ !!! music//p' | sort > data/articlesSansPortail-musique-$1.txt) \
    > >(sed -n 's/ !!! actor//p' | sort > data/articlesSansPortail-acteurs-$1.txt) \
    > >(sed -n 's/ !!! homo//p' | sort > data/articlesSansPortail-homo-$1.txt) \
    > >(grep -v '\!\!\! \(music\|actor\|homo\)' | sort > data/articlesSansPortail-$1.txt) &

{ pv data/articlesSansInfobox-full-$1.txt } \
    > >(sed -n 's/ !!! music//p' | sort > data/articlesSansInfobox-musique-$1.txt) \
    > >(sed -n 's/ !!! actor//p' | sort > data/articlesSansInfobox-acteurs-$1.txt) \
    > >(grep -v '\!\!\! \(music\|actor\)' | sort > data/articlesSansInfobox-$1.txt) &

#python noiw.py data/wikidatawiki-20130505.xml | sort -rn > data/articlesACreer-20130505.txt

wait

echo 'Finished processing'
notify-send -u normal -t 6000 "Finished processing" -i /usr/share/icons/gnome/48x48/actions/gtk-execute.png
