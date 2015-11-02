#! /usr/bin/awk -f

/<title>.*?</ {
  title = substr($0, 12, length($0) - 19)
}

/[Aa]rkan?([^a-zA-Z]|osis)/ {
  if (index(title, ":")) {
    print title " ||| " $0
  }
}
