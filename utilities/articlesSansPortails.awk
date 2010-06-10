#! /bin/awk -f

BEGIN {
  portal = 1
}

END {
  if (!portal) {
    print title
  }
}

/<title>.*?</ {
  if (!portal) {
    print title
  }

  title = substr($0, 12, length($0) - 19)
  portal = match(title, /^(Aide|Catégorie|Fichier|MediaWiki|Modèle|Portail|Projet|Référence|Wikipédia)/)
}

tolower($0) ~ /(#redirect|{{portail|{{homonymie|{{disambig)/ {
  portal = 1
}
