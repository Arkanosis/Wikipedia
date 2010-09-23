#! /usr/bin/awk -f

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

tolower($0) ~ /(#redirect|{{portail|{{homonymie|{{disambig|{{bandeau[ _]standard[ _]pour[ _]page[ _]d'homonymie|arrondissements[ _]homonymes|batailles[ _]homonymes|cantons[ _]homonymes|communes[ _]françaises[ _]homonymes|films[ _]homonymes|gouvernements[ _]homonymes|internationalisation|isomérie|lieux[ _]homonymes|paronymie|patronyme|patronymie|personnes[ _]homonymes|saints[ _]homonymes|sigle|titres[ _]homonymes|toponymie|unités[ _]homonymes|villes[ _]homonymes)/ {
  portal = 1
}
