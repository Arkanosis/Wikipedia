#! /bin/sh

for lang in aa ab af am ar as ay ba be bg bi bn bo br ca co cs cy da de el en es es et eu fa fi fj fo fr fy ga gd gl gn ha he hi hr hu hy id is it iu ja jw ka kk kl km kn ko ks ku la ln lo lt lv mg mi mk ml mn mo mr ms mt my ne nl no oc om or pa pl ps pt qu rn ro ru rw sa sd sg sh si sk sl sm sn so sq ss su sv sw ta te tg th ti tk tl to tr ts tt tw ug uk ur uz vi wo xh yi yo za zh zu; do
    url="http://download.wikimedia.org/${lang}wiki/latest/${lang}wiki-latest-pages-articles.xml.bz2"
    echo downloading $url
    wget $url -O ${lang}wiki.xml.bz2
done

echo finished
