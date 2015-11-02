#! /usr/bin/awk -f

END {
  print time " || " type " || " title " || " user " || " homo
}

/<title>.*?</ {
  if (title) {
    print time " || " type " || " title " || " user " || " homo
  }

  title = substr($0, 12, length($0) - 19)
  if (match(title, /^(Aide|Catégorie|Fichier|MediaWiki|Modèle|Portail|Projet|Référence|Wikipédia)/)) {
    title = 0
  }
  homo = "article"
  next
}

/<timestamp>.*?</ {
  time = substr($0, 18, length($0) - 39)
  next
}

/<redirect.*?\/>/ {
  title = 0
  next
}

/<username>.*?</ {
  type = "user"
  user = substr($0, 19, length($0) - 29)
  next
}

/<ip>.*?</ {
  type = "ip"
  user = substr($0, 13, length($0) - 17)
  next
}

tolower($0) ~ /({{homonymie|{{disambig|{{bandeau[ _]standard[ _]pour[ _]page[ _]d'homonymie|arrondissements[ _]homonymes|batailles[ _]homonymes|cantons[ _]homonymes|communes[ _]françaises[ _]homonymes|films[ _]homonymes|gouvernements[ _]homonymes|internationalisation|isomérie|lieux[ _]homonymes|paronymie|patronyme|patronymie|personnes[ _]homonymes|saints[ _]homonymes|sigle|titres[ _]homonymes|toponymie|unités[ _]homonymes|villes[ _]homonymes)/ {
  homo = "homo"
  next
}
