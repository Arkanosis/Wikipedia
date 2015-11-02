#! /usr/bin/awk -f

BEGIN {
  nb = 0
}

END {
  print nb " articles"
}

/<title>.*?</ {
  ++nb

  title = substr($0, 12, length($0) - 19)
  if (match(title, /^(Aide|Catégorie|Fichier|MediaWiki|Modèle|Portail|Projet|Référence|Wikipédia)/)) {
    --nb
  }

  if (!(nb % 10000)) {
    print nb " articles"
  }
  next
}

/<redirect \/>/ {
  --nb
  next
}
