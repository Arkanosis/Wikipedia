#! /usr/bin/awk -f

# TODO un autre script pour vérifier que toutes les pages en « (homonymie) » on bien un modèle correspondant

BEGIN {
  redirect = 1
}

END {
  if (!link) {
    print title
  }
}

/<title>[^(]*\(Homonymie\)</ {
  if (!redirect) {
    print title
  }

  title = substr($0, 12, length($0) - 19)
  redirect = match(title, /^(Aide|Catégorie|Fichier|MediaWiki|Modèle|Portail|Projet|Référence|Wikipédia)/)
}

tolower($0) ~ /#redirect/ {
  redirect = 1
}
