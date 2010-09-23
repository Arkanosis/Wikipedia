#! /bin/sh

for lang in aa ab ace af ak als am an ang ar arc arz as ast av ay az ba bar bat-smg bcl be be-x-old bg bh bi bm bn bo bpy br bs bug bxr ca cbk-zam cdo ce ceb ch chr chy ckb co cr crh cs csb cu cv cy da de diq dsb dv dz ee el eml en eo es et eu ext fa ff fi fiu-vro fj fo fr frp fur fy ga gan gd gl glk gn got gu gv ha hak haw he hi hif hr hsb ht hu hy ia id ie ig ik ilo io is it iu ja jbo jv ka kaa kab kg ki kk kl km kn ko ks ksh ku kv kw ky la lad lb lbe lg li lij lmo ln lo lt lv map-bms mdf mg mhr mi mk ml mn mr ms mt mwl my myv mzn na nah nap nds nds-nl ne new ng nl nn no nov nrm nv ny oc om or os pa pag pam pap pcd pdc pi pih pl pms pnb pnt ps pt qu rm rmy rn ro roa-rup roa-tara ru rw sa sah sc scn sco sd se sg sh si simple sk sl sm sn so sq sr srn ss st stq su sv sw szl ta te tet tg th ti tk tl tn to tpi tr ts tt tum tw ty udm ug uk ur uz ve vec vi vls vo wa war wo wuu xal xh yi yo za zea zh zh-classical zh-min-nan zh-yue zu; do
    url="http://download.wikimedia.org/${lang}wiki/latest/${lang}wiki-latest-pages-articles.xml.bz2"
    if ! [ -f ${lang}wiki.xml ]; then
	echo downloading $url
	wget -q $url -O - | bunzip2 > ${lang}wiki.xml
    else
	echo already downloaded $url
    fi
done

echo finished
