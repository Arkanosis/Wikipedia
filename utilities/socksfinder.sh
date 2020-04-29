#! /bin/sh

# socksfinder v0.1
# Copyright (C) 2020 Jérémie Roquet <jroquet@arkanosis.net>
# Licensed under the ISC license

usage() {
    cat <<EOF
Usage: ./socksfinder.sh build
       ./socksfinder.sh query User1 User2 User3
EOF
}

build() {
    if [ -f postings.gz ]; then
        echo 'Postings already built, nothing to do'
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

    echo 'Postings built'
}

query() {
    if ! [ -f postings.gz ]; then
        echo 'Dowloading pre-built postings...'
        curl https://arkanosis.fr/wikipedia/socksfinder/postings.gz -o postings.gz
        echo 'Postings downloaded'
    fi

    names="$(mktemp -p .)"

    for name in "$@"; do
        echo "$name|"
    done > "$names"

    matches="$(mktemp -p .)"

    gunzip -c postings.gz |
        grep -Ff "$names" > "$matches"

    sed 's@^[^|]\+|@@' "$matches" |
        sort |
        uniq -c |
        sort -nrk1 |
        awk '
    $1 < 2 {
        exit
    }
    1' |
        while read count title; do
            echo $count $title '('$(
                sed -n "s@^\([^|]\+\)|$title\$@ \1@p" "$matches" |
                    tr '\n' ','
                 ) ')'
        done

    rm "./$names"
    rm "./$matches"
}

if [ "$#" -eq 0 ]; then
    usage
else
    case "$1" in
        help|-h|--help)
            usage
        ;;
        version|--version)
            echo 'socksfinder v0.1'
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
