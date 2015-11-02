#! /usr/bin/zsh

if ((# < 1)); then
  echo 'Usage: sulcount.sh <login>' >&2
  exit 1
fi

wget -q -O - "https://tools.wmflabs.org/quentinv57-tools/tools/sulinfo.php?username=$1&showlocked=1" | sed -n 's@^\s\+<td>\([a-z0-9_]\+\)</td>$@\1@p' | sort
