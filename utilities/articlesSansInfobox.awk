#! /usr/bin/awk -f

function print_or_not() {
  if (!infobox) {
    if (music) {
      print title " !!! music"
    }
    if (actor) {
      print title " !!! actor"
    }
    if (!music && !actor) {
      print title
    }
  }
}

BEGIN {
  infobox = 1
  music = 0
  actor = 0
  homo = 0
}

END {
  print_or_not()
}

/<title>.*?</ {
  print_or_not()

  title = substr($0, 12, length($0) - 19)
  infobox = match(title, /^(Aide|Catégorie|Fichier|MediaWiki|Modèle|Portail|Projet|Référence|Wikipédia)/)
  music = 0
  actor = 0
  homo = 0
  next
}

tolower($0) ~ /(#redirect|{{infobox|{{homonymie|{{disambig|{{bandeau[ _]standard[ _]pour[ _]page[ _]d'homonymie|arrondissements[ _]homonymes|batailles[ _]homonymes|cantons[ _]homonymes|communes[ _]françaises[ _]homonymes|films[ _]homonymes|gouvernements[ _]homonymes|internationalisation|isomérie|lieux[ _]homonymes|paronymie|patronyme|patronymie|personnes[ _]homonymes|saints[ _]homonymes|sigle|titres[ _]homonymes|toponymie|unités[ _]homonymes|villes[ _]homonymes)/ {
  infobox = 1
  next
}

tolower($0) ~ /cat[ée]gor(y|ie) *?: *?album[ _]musical/ {
  music = 1
  next
}

tolower($0) ~ /cat[ée]gor(y|ie) *?: *?act(eur|rice)/ {
  actor = 1
  next
}
