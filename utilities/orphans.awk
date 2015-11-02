#! /usr/bin/awk -f

BEGIN {

}

/<title>.*?</ {
  if ($0 ~ /<title>Discussion:/) {
    print substr($0, 23, length($0) - 30) " !!!"
  } else if (!($0 ~ /<title>(Aide|Catégorie|Fichier|MediaWiki|Modèle|Portail|Projet|Utilisateur|Référence|Wikipédia|Discussion aide|Discussion catégorie|Discussion fichier|Discussion mediawiki|Discussion modèle|Discussion portail|Discussion projet|Discussion utilisateur|Discussion référence|Discussion Wikipédia):/)) {
    print substr($0, 12, length($0) - 19)
  }
}

{

}
