#! /usr/bin/awk -f

BEGIN {
  synonyms_count = 0
  consider = 0
  consider_synonyms = 0
}

END {
  display_synonyms()
}

/<title>.*?</ {
  if (!match(title, /^(Aide|Catégorie|Fichier|MediaWiki|Modèle|Portail|Projet|Référence|Wiktionnaire)/)) {
    display_synonyms()
  }

  title = substr($0, 12, length($0) - 19)
}

/{{-(adj|adv|aff|art|aux|conj|interf|interj|lettre|loc|nom|onoma|part|post|préf|prénom|prép|pronom|prov|racine|radical|sigle|sin|suf|symb|verb)-/{
  consider = 0
}

/{{-adj-\|fr}}/ {
  consider = 1
}

{
  if (consider_synonyms) {
    if (match ($0, /^\*+ \[\[.*?\]\]/)) {
      synonyms[synonyms_count++] = $0
    } else if (match ($0, /^ *$/)) {

    } else {
      consider_synonyms = 0
    }
  }
}

/{{-syn-}}/{
  if (consider) {
    consider_synonyms = 1
  }
}

function display_synonyms() {
  if (synonyms_count) {
    printf "== %s ==\n", title
    for (synonym in synonyms) {
      print synonyms[synonym]
    }
    synonyms_count = 0
    delete synonyms
  }
}