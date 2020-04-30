#! /bin/sh

# socksfinder v0.1
# Copyright (C) 2020 Jérémie Roquet <jroquet@arkanosis.net>
# Licensed under the ISC license

VERSION='socksfinder v0.2.1'

export LANG=C
export LC_ALL=C

DEBUG=false
if [ $# -gt 0 ] && [ "x$1" = 'x--debug' ]; then
    DEBUG=true
    shift
fi

debug() {
    if $DEBUG; then
        echo "debug: $@" >&2
    fi
}

usage() {
    cat <<EOF
Usage: ./socksfinder.sh build
       ./socksfinder.sh query User1 User2 User3
EOF
}

build() {
    if [ -f postings.gz ]; then
        echo 'Postings already built, nothing to do' >&2
        return
    fi

    curl https://dumps.wikimedia.org/frwiki/20200420/frwiki-20200420-stub-meta-history.xml.gz  |
        gunzip |
        sed -n 's@^ *<title>\([^<]\+\)</title>$@P \1@p ; s@^ *<username>\([^ ]\+\)</username>@U \1@p' |
        awk '
    $1 == "P" {
        page = substr($0, 3)
    }
    $1 == "U" {
        print(substr($0, 3) "|" page)
    }
    ' | sort -u |
        gzip --best > postings.gz

    echo 'Postings built' >&2
}

query() {
    debug "Using $VERSION"

    if ! [ -f postings.gz ]; then
        echo 'Dowloading pre-built postings...' >&2
        curl https://arkanosis.fr/wikipedia/socksfinder/postings.gz -o postings.gz
        echo 'Postings downloaded' >&2
    fi

    debug "postings checksum is $(sha256sum postings.gz | cut -d ' ' -f 1)"

    names="$(mktemp -p .)"

    for name in "$@"; do
        echo "$name|"
    done > "$names"

    debug "$(wc -l "$names" | cut -d ' ' -f 1) names to lookup (in $names)"

    matches="$(mktemp -p .)"

    gunzip -c postings.gz |
        grep -Ff "$names" > "$matches"

    debug "$(wc -l "$matches" | cut -d ' ' -f 1) matches found (in $matches)"

    results="$(mktemp -p .)"

    sed 's@^[^|]\+|@@' "$matches" |
        sort |
        uniq -c |
        sort -nrk1 > "$results"

    debug "$(wc -l "$results" | cut -d ' ' -f 1) results found (in $results)"

    coresults="$(mktemp -p .)"

    awk '
    $1 < 2 {
        exit
    }
    1' > "$coresults" < "$results"

    debug "$(wc -l "$coresults" | cut -d ' ' -f 1) coresults found (in $coresults)"

    while read count title; do
        echo $count $title '('$(
            sed -n "s@^\([^|]\+\)|$title\$@ \1@p" "$matches" |
                tr '\n' ','
             ) ')'
    done < "$coresults"

    if ! $DEBUG; then
        rm "./$names"
        rm "./$matches"
        rm "./$results"
        rm "./$coresults"
    fi
}

if [ "$#" -eq 0 ]; then
    usage
else
    case "$1" in
        help|-h|--help)
            usage
        ;;
        version|--version)
            echo "$VERSION"
        ;;
        build)
            build
        ;;
        query)
            shift
            query "$@"
        ;;
        *)
            usage >&2
            exit 1
        ;;
    esac
fi
