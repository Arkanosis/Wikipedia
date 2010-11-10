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
    print title
  }

  class = 0
  title = substr($0, 12, length($0) - 19)
}

/class=&quot;([^&]* )?video(&quot;| )/ {
  class = 1
}
