#! /usr/bin/awk -f

BEGIN {

}

END {

}

/<title>Discussion:.*?</ {
  if (eval) {
    print title
    print " ⇒ " eval
  }
  title = substr($0, 23, length($0) - 30)
  eval = ""
}

/({{[Ww]ikiprojet|avancement|importance)=/ {
  eval = eval " " $0
}
