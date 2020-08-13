#! /usr/bin/awk -f

function print_or_not() {
  if (!portal) {
    if (music) {
      print title " !!! music"
    }
    if (actor) {
      print title " !!! actor"
    }
    if (homo) {
      print title " !!! homo"
    }
    if (!music && !actor && !homo) {
      print title
    }
  }
}

BEGIN {
  portal = 1
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
  portal = match(title, /^(Aide|Catégorie|Fichier|MediaWiki|Modèle|Module|Portail|Projet|Référence|Sujet|Wikipédia)/)
  music = 0
  actor = 0
  homo = 0
  next
}

tolower($0) ~ /(#redirect|{{portail|{{homonyme|{{homonymie|{{disambig|{{bandeau[ _]standard[ _]pour[ _]page[ _]d'homonymie|{{abbayes[ _]homonymes|{{arrondissements[ _]homonymes|{{batailles[ _]homonymes|{{cantons[ _]homonymes|{{communes[ _]françaises[ _]homonymes|{{édifices[ _]religieux[ _]homonymes|{{films[ _]homonymes|{{hydronymie|{{gouvernements[ _]homonymes|{{guerres[ _]homonymes|{{internationalisation|{{isomérie|{{monastères[ _]homonymes|{{prieurés[ _]homonymes|{{paronymie|{{patronyme|{{patronymie|{{personnes[ _]homonymes|{{prénoms[ _]homonymes|{{saints[ _]homonymes|{{sigle|{{surnoms[ _]homonymes|{{titres[ _]homonymes|{{toponymie|{{unités[ _]homonymes|{{villes[ _]homonymes|{{voir[ _]homonymes|{{rues[ _]homonymes|{{place[ _]ou[ _]square[ _]homonyme)/ {
  portal = 1
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

tolower($0) ~ /cat[ée]gor(y|ie) *?: *?homonymie/ {
  homo = 1
  next
}
