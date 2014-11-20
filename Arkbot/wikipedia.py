# -*- coding: utf-8 -*-

# Wikipedia
# (C) 2010 Arkanosis
# jroquet@arkanosis.net

# http://github.com/Arkanosis/Wikipedia/Arkbot

# Ce script est dans le domaine public

_wikis = [
	'aa', 'ab', 'ace', 'af', 'ak', 'als', 'am', 'an', 'ang', 'ar', 'arc', 'arz', 'as', 'ast', 'av', 'ay', 'az',
	'ba', 'bar', 'bat-smg', 'bcl', 'be', 'be-x-old', 'bg', 'bh', 'bi', 'bm', 'bn', 'bo', 'bpy', 'br', 'bs', 'bug', 'bxr',
	'ca', 'cbk-zam', 'cdo', 'ce', 'ceb', 'ch', 'cho', 'chr', 'chy', 'ckb', 'co', 'cr', 'crh', 'cs', 'csb', 'cu', 'cv', 'cy',
	'da', 'de', 'diq', 'dk', 'dsb', 'dv', 'dz',
	'ee', 'el', 'eml', 'en', 'eo', 'es', 'et', 'eu', 'ext',
	'fa', 'ff', 'fi', 'fiu-vro', 'fj', 'fo', 'fr', 'frp', 'fur', 'fy',
	'ga', 'gan', 'gd', 'gl', 'glk', 'gn', 'got', 'gu', 'gv',
	'ha', 'hak', 'haw', 'he', 'hi', 'hif', 'ho', 'hr', 'hsb', 'ht', 'hu', 'hy', 'hz',
	'ia','id', 'ie', 'ig', 'ii', 'ik', 'ilo', 'io', 'is', 'it', 'iu',
	'ja', 'jbo', 'jv',
	'ka', 'kaa', 'kab', 'kg', 'ki', 'kj', 'kk', 'kl', 'km', 'kn', 'ko', 'kr', 'ks', 'ksh', 'ku', 'kv', 'kw', 'ky',
	'la', 'lad', 'lb', 'lbe', 'lg', 'li', 'lij', 'lmo', 'ln', 'lo', 'lt', 'lv',
	'map-bms', 'mdf', 'meta', 'mg', 'mh', 'mhr', 'mi', 'mk', 'ml', 'mn', 'mo', 'mr', 'ms', 'mt', 'mus', 'mwl', 'my', 'myv', 'mzn',
	'na', 'nah', 'nan', 'nap', 'nb', 'nds', 'nds-nl', 'ne', 'new', 'ng', 'nl', 'nn', 'no', 'nov', 'nrm', 'nv', 'ny',
	'oc', 'om', 'or', 'os',
	'pa', 'pag', 'pam', 'pap', 'pcd', 'pdc', 'pi', 'pih', 'pl', 'pms', 'pnb', 'pnt', 'ps', 'pt',
	'qu',
	'rm', 'rmy', 'rn', 'ro', 'roa-rup', 'roa-tara', 'ru', 'rw',
	'sa', 'sah', 'sc', 'scn', 'sco', 'sd', 'se', 'sg', 'sh', 'si', 'simple', 'sk', 'sl', 'sm', 'sn', 'so', 'sq', 'sr', 'srn', 'ss', 'st', 'stq', 'su', 'sv', 'sw', 'szl',
	'ta', 'te', 'tet', 'tg', 'th', 'ti', 'tk', 'tl', 'tn', 'to', 'tokipona', 'tp', 'tpi', 'tr', 'ts', 'tt', 'tum', 'tw', 'ty',
	'udm', 'ug', 'uk', 'ur', 'uz',
	've', 'vec', 'vi', 'vls', 'vo',
	'wa', 'war', 'wo', 'wuu',
	'xal', 'xh',
	'yi', 'yo',
	'za', 'zea', 'zh', 'zh-classical', 'zh-cn', 'zh-min-nan', 'zh-tw', 'zh-yue', 'zu',
]
