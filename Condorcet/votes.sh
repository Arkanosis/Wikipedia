#! /bin/zsh

# Attention !
# Ne prend pas en compte les votes sans '>' !

if ((# < 2)); then
    echo 'Usage: votes.sh <page> <outputFile>' >&2
    exit 1
fi

wget "http://fr.wikipedia.org/wiki/$1" -O - 2> /dev/null | sed -n 's/&gt;/>/gp' | sed -n 's@<li>\([ 	[:upper:]=,>]\{2,\}\).*<a href="[^"]\+" title="\(Discussion \)\?[uU]tilisateur:\([^"]\+\)".\+@\1 | \3@p' >| $2
