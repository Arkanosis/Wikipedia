#! /bin/zsh

if ((# < 2)); then
    echo 'Usage: getLinksFromArticles.sh <articles> <outputFile>' >&2
    exit 1
fi

for article in $@[1,-2]; do
    wget "http://fr.wikipedia.org/w/index.php?title=$article&action=raw" -O - 2> /dev/null
done | sed '
  s/\[\[/\n[[/g
  s/\]\]/]]\n/g
  s/\[\[[^]]\+:[^]]\+\]\]//g
  s/\[\[\([^]]\+\)|[^]]\+\]\]/\1/g
' | sed -n 's/\[\[\([^]]\+\)\]\]/\1/p' | sort -uf >| $@[-1]
