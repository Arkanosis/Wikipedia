#! /usr/bin/awk -f

BEGIN {
  count = 0
}

END {
  print count " || " title
}

/<title>.*?</ {
  if (count) {
    print count " || " title
    count = 0
  }

  title = substr($0, 12, length($0) - 19)
}

/<revision>/ {
  ++count
}
