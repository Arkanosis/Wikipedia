#! /usr/bin/awk -f

/<title>.*?</ {
  title = substr($0, 12, length($0) - 19)
  next
}

/<text( bytes="[0-9]+")?( xml:space="preserve")? \/>/ {
  print title
  next
}

/<text( bytes="[0-9]+")?( xml:space="preserve")?>/ {
  if (match($0, /<text( bytes="[0-9]+")?( xml:space="preserve")?>[[:space:]]*<\/text>/)) {
    print title
  } else if (match($0, /<text( bytes="[0-9]+")?( xml:space="preserve")?>(.*)/, matches)) {
    text = matches[3]
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
