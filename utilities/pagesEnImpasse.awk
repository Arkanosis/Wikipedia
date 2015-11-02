#! /usr/bin/awk -f

BEGIN {
  link = 1
}

END {
  if (!link) {
    print title
  }
}

/<title>.*?</ {
  if (!link) {
    print title
  }

  title = substr($0, 12, length($0) - 19)
  link = match(title, /^(Aide|Catégorie|Fichier|MediaWiki|Modèle|Module|Portail|Projet|Référence|Sujet|Wikipédia)/)
}

tolower($0) ~ /(#redirect|{{portail|{{homonymie|{{disambig|{{bandeau[ _]standard[ _]pour[ _]page[ _]d'homonymie|arrondissements[ _]homonymes|batailles[ _]homonymes|cantons[ _]homonymes|communes[ _]françaises[ _]homonymes|films[ _]homonymes|gouvernements[ _]homonymes|internationalisation|isomérie|lieux[ _]homonymes|paronymie|patronyme|patronymie|personnes[ _]homonymes|saints[ _]homonymes|sigle|titres[ _]homonymes|toponymie|unités[ _]homonymes|villes[ _]homonymes)/ {
  link = 1
}

/\[\[.*\]\]/ {
  link = 1
}
