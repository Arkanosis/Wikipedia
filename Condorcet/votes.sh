#! /bin/zsh

# Attention !
# Ne prend pas en compte les votes sans '>' !

if ((# < 2)); then
    echo 'Usage: votes.sh <page> <outputFile>' >&2
    exit 1
fi

wget "http://fr.wikipedia.org/wiki/$1" -O - 2> /dev/null |
  sed -n '
    s/&gt;/>/gp
    /^<h[2-6]>.\+<\/h[2-6]>$/p
  ' | sed -n '
    s@<li>\(\([[:upper:]0-9]\+[ 	]*[=,>][ 	]*\)\+[[:upper:]0-9]\+\).*<a href="[^"]\+" title="\(Discussion \)\?[uU]tilisateur:\([^/"]\+\)".\+@\1|\4@p  ; /^=.\+=$/p
    /^<h[2-6]>.\+<\/h[2-6]>$/p
  ' | sed '
    s/modifier//
    t tag
    s/,/=/g ; s/[ 	]//g ; s/[>=|]/ & /g
    :tag
      s/<[^>]\+>//
      t tag
  ' >| $2
