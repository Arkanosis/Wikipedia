#! /bin/zsh

if ((# < 2)); then
    echo 'Usage: getArticlesFromCategory.sh <category> <outputFile>' >&2
    exit 1
fi

prefix="http://fr.wikipedia.org/w/index.php?title=Catégorie:$1"
url=$prefix
tmp=`tempfile`

echo -n >| $2

while [[ -n $url ]]; do
    echo "Processing $url"
    wget "$url" -O - 2> /dev/null > $tmp
    < $tmp sed -n 's@.*<li><a href="/wiki/\([a-zA-Z0-9%_]\+\)".*@\1@p' >> $2
    url=$prefix`< $tmp sed -n '/200/ s@.*&amp;from=\([a-zA-Z0-9%_+]\+\).*@\&from=\1@p' | head -n 1`
done

rm -f $tmp
