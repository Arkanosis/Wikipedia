#! /bin/zsh

if ((# < 1)); then
    echo 'Usage: liensExternes.sh <dump>' >&2
    exit 1
fi

< $1 awk '
BEGIN {
  count = 0
  title = ""
  skip = 1
  ref = 0
}

/<title>.*?</ {
  if (!skip) {
    print(count, title)
  }

  count = 0
  title = substr($0, 12, length($0) - 19)
  skip = match(title, /^(Aide|Catégorie|Fichier|MediaWiki|Modèle|Portail|Projet|Référence|Wikipédia)/)
}

/\<ref.*http:\/\// {
  ref = 1
}

/http:\/\// {
  if (!ref) {
    count += 1
  }
}

/<\/ref>/ {
  ref = 0
}

' | sort -nr
