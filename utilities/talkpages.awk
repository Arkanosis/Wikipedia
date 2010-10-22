#! /usr/bin/awk -f

BEGIN {
  left = 0
  max = 20
  skip = 10
}

/<title>.*?</ {
  if ($0 ~ /<title>Discussion:/) {
    left = max + skip
    print $0
  } else {
    left = 0
  }
}

{
  if (left) {
    if (left < max) {
      print $0
    }
    left -= 1
  }
}
