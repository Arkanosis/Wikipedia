#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-

# Wikitext manipulations
# (C) 2010 Arkanosis
# arkanosis@gmail.com

# http://github.com/Arkanosis/Wikipedia/Arkbot

# Ces fonctions sont mises à disposition sous licence MIT
# http://www.opensource.org/licenses/mit-license.php

# TODO
# 1- extract: wikitext → [('template', {'arg': 'value', 'arg2', 'value2'}, fulltext)]
# 2- query: wikitext, '/template'  → [({'arg': 'value', 'arg2', 'value2'}, fulltext)]
#           wikitext, '/template/arg' → [value1, value2]
# 3- remap: wikitext, {'/template/arg': }

import re

def _reg(exp):
    return re.compile(exp, re.DOTALL | re.UNICODE)

_templates = _reg(u'\{\{((?:(?!\{\{).)+?)\}\}')
_template = _reg(u'^\s*(?P<name>[^\|]+?)\s*(?P<parameters>\|.*?)?$')
_parameters = _reg(u'\s*(?P<fullText>\|\s*(?:(?P<name>[^|=]+)=)?(?P<value>[^\|]*))')

def check(text):
    for special in ['${', '$}', '$!']:
        assert(special not in text)

def decode(text):
    return text.replace('${', '{{').replace('$}', '}}').replace('$!', '|')

def extractParameters(text):
    template = _template.match(text)
    name = template.group('name').strip()
    parameters = template.group('parameters')
    if parameters:
        return name.strip(), [(name.strip(), decode(value.strip()), decode(fullText.strip())) for fullText, name, value in _parameters.findall(parameters)]
    else:
        return name, []
    parameters = []

def extractTemplates(text):
    check(text)
    result = []
    while True:
        templates = _templates.findall(text)
        if not templates:
            break
        for template in templates:
            fullText = '{{%s}}' % template
            result.append((extractParameters(template), decode(fullText)))
            text = text.replace(fullText, '${%s$}' % template.replace('|', '$!'))
    return result

def replaceTemplate(text, templateName, replace):
    for template in extractTemplates(text):
        if template[0][0] == templateName:
            text = text.replace(template[1], replace(template[0][1]))
    return text

def replaceTemplates(text, mappings):
    for template, replacement in mappings.items():
        text = replaceTemplate(text, template, replacement)
    return text

# ---- test on file ----

import sys

def convertIBoxChefdEtat(params):
    # TODO convert params to dictionary, with parameter mapping
    res = """{{Infobox Politicien/début
| nom = %(nom)
}}
""" % params
    for fonction in ():
        res += """{{Infobox Politicien/fonction
| début = %(début)
}}
""" % params
    return res + """{{Infobox Politicien/fin
| nom complet = %(nom complet)
}}""" % params


mappings = {
    'Infobox Premier ministre': convertIBoxPremierMinistre,
    'Infobox Chef d\'État': convertIBoxChefdEtat,
    'Infobox Gouverneur': convertIBoxGouverneur,
    'Infobox Monarque': convertIBoxMonarque,
}

with open(sys.argv[1]) as source:
    print replaceTemplates(source.read(), mappings)

sys.exit(0)

# ---- test on string ----

text = """
{{Infobox test test
| nom = Foo bar
| date de naissance = {{date|foo|bar|id=magic}}
}}
Foo bar né le {{date|foo|bar|id=magic}} à {{USA}}.

{{Palette|Foo}}
{{Portail|Bar|Baz}}

{{Commonscat|theme=reloaded
|      var  = iable
|end}}
"""

#for template in extractTemplates(text):
#    print '< "%s" [%s]' % (template[0][0], template[1])
#    for parameter in template[0][1]:
#        print '  "%s": "%s" [%s]' % (parameter[0], parameter[1], parameter[2])

def xmlize(name):
    def _xmlize(params):
        res = '<%s ' % name
        for param in params:
            if param[0]:
                res += '%s="%s" ' % (param[0], param[1])
            else:
                res += '%s="true" ' % param[1]
        return res + '/>'
    return _xmlize

def jsonize(name):
    def _jsonize(params):
        res = '%s = {\n' % name
        for param in params:
            if param[0]:
                res += '\t\'%s\': \'%s\',\n' % (param[0], param[1])
            else:
                res += '\t\'%s\': True,\n' % param[1]
        return res + '}'
    return _jsonize

mappings = {
    'Commonscat': xmlize('commonscat'),
    'date': xmlize('time'),
    'Infobox test test': jsonize('ibox'),
}

print '-------------'
print text
print '-------------'
print replaceTemplates(text, mappings)
print '-------------'
