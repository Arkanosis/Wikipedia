#! /usr/bin/awk -f

/<title>.*?</ {
  title = substr($0, 12, length($0) - 19)
  next
}

/<text xml:space="preserve" \/>/ {
    print title
    next
}

/<text xml:space="preserve">/ {
  text = substr($0, 34)

  if (match($0, /<\/text>/)) {
    if (match(substr(text, 0, length(text) - 7), /^[[:space:]]*$/)) {
      print title
    }
  }

  next
}

{
  text = text $0
}

/<\/text>/ {
  if (match(substr(text, 0, length(text) - 7), /^[[:space:]]*$/)) {
    print title
  }
}
