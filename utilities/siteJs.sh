#! /usr/bin/zsh

#grep '<title>MediaWiki:.*\.js</title>' data/frmetawiki-$1.xml > data/sitejs/index.txt

# TODO escape

while read script; do
    wget --header="accept-encoding: gzip" http://fr.wikipedia.org/w/index.php\?title=$script\&action=raw -O - | gunzip -c > data/sitejs/${${script#MediaWiki:}/\//_}
done < data/sitejs/index.txt
