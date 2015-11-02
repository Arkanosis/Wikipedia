#! /usr/bin/awk -f

BEGIN {
  class = 0
}

END {
  if (class) {
    print title
  }
}

/<title>.*?</ {
  if (class) {
    print title " " str
  }

  class = 0
  title = substr($0, 12, length($0) - 19)
}

/class=(&quot;)?([^&]*[^a-zA-Z0-9])?interprojet[^a-zA-Z0-9]/ {
  class = 1
  str = $0
}
