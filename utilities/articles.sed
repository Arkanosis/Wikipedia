#! /bin/sed -nf

s@\s\+<title>\([^\(\(M.dia\|Sp.cial\|Wikip.dia\|Projet\|Portail\|Aide\|Fichier\|Image\|Cat.gorie\|Mod.le\|MediaWiki\|R.f.rence\):\)][^<]\+\)</title>@\1@p
