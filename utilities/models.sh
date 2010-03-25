#! /bin/zsh

wget -O - 'http://fr.wikipedia.org/w/index.php?title=Sp%C3%A9cial%3AIndex&prefix=abusefilter-warning-&namespace=8' 2> /dev/null | sed -n '
  /mw-prefixindex-nav-form/ {
    :r
      s@<td><a href="/wiki/MediaWiki:Abusefilter-warning-[^"]\+" title="MediaWiki:Abusefilter-warning-[^"]\+">\(Abusefilter-warning-[^<]\+\)</a></td>@\1\n@p
      t r
  }
' | sed -n 's/\(.\+>\)\?\([^<>]\+\)\(<.\+\)\?/\2/p' | sort -u | head -n -1 | while read article; do

echo "== [[MediaWiki:$article]] =="
echo
echo "{{MediaWiki:$article}}"
echo

done