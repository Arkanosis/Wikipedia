/*
***************************************************************************
** xpatrol - Permet d'effectuer rapidement certaines actions en patrouille
**   - marquer une révision comme relue sans changer de page
**   - blanchir une page
**   - ajouter un bandeau à une page
**   - masquer les pages déjà blanchies dans la liste des nouvelles pages
** Compatibilité : frwiki uniquement
** Support : Discussion_utilisateur:Arkanosis
** Licence : MIT/X11
**
** Installation : ajouter
**  importScript('Utilisateur:Arkanosis/xpatrol.js');
** dans le monobook.js
*/

if (typeof (xpatrolEnableClear) == 'undefined')
  var xpatrolEnableClear = false;
if (typeof (xpatrolEnableBanner) == 'undefined')
  var xpatrolEnableBanner = false;
if (typeof (xpatrolWatchMain) == 'undefined')
  var xpatrolWatchMain = false;
if (typeof (xpatrolWatchOthers) == 'undefined')
  var xpatrolWatchOthers = false;

var xpatrolEmptyNewPagesNextState = 0;
var xpatrolEmptyNewPagesToggleTexts = [ 'afficher', 'masquer' ];
var xpatrolEmptyNewPagesStates = [ 'none', 'list-item' ];

function month(id)
{
  return  ['janvier', 'février', 'mars', 'avril', 'mai', 'juin', 'juillet', 'août', 'septembre', 'octobre', 'novembre', 'décembre'][id];
}

function xpatrolToggleEmptyNewPages()
{
  var lis = document.getElementsByTagName('li');
  for (var liId = 0; liId < lis.length; ++liId)
    if (lis[liId].innerHTML.indexOf('[0 octet]') != -1)
    {
      lis[liId].style.display = xpatrolEmptyNewPagesStates[xpatrolEmptyNewPagesNextState];
    }
    document.getElementById('xpatrol-ToggleEmptyNewPages').innerHTML = xpatrolEmptyNewPagesToggleTexts[xpatrolEmptyNewPagesNextState];
    xpatrolEmptyNewPagesNextState = !xpatrolEmptyNewPagesNextState + 0;
}

function xpatrolCheck(url, tag)
{
  var request = new XMLHttpRequest();
  request.open('GET', wgServer + url, false);
  request.send('');

  var elts = document.getElementsByTagName(tag);
  for (var eltId = 0; eltId < elts.length; ++eltId)
    if (elts[eltId].className == 'patrollink')
    {
      elts[eltId].childNodes[1].innerHTML = '<img src="http://upload.wikimedia.org/wikipedia/commons/thumb/f/fb/Yes_check.svg/15px-Yes_check.svg.png" /> Révision marquée comme relue';
      return;
    }
}

function xpatrolEdit(article, text, reason, button)
{
  var request = new XMLHttpRequest();
  request.open('GET', wgServer + wgScriptPath + '/index.php?title=' + encodeURIComponent(article) + '&action=edit', false);
  request.send('');

  var parser = new DOMParser();
  var response = parser.parseFromString(request.responseText, 'application/xhtml+xml');

  if (text)
  {
    var previousText = response.getElementById('wpTextbox1').value;
    text = text.replace('$$text$$', previousText);
  }

  var inputs = response.getElementById('editform').getElementsByTagName('input');
  for (inputId = 0; inputId < inputs.length; ++inputId)
    switch (inputs[inputId].name)
    {
      case 'wpStarttime':
        var wpStarttime = inputs[inputId].value;
        break;
      case 'wpEdittime':
        var wpEdittime = inputs[inputId].value;
        break;
      case 'wpEditToken':
        var wpEditToken = inputs[inputId].value;
        break;
      default:
        break;
    }

  var parameters = 'wpSave=1'
    + '&wpTextbox1=' + encodeURIComponent(text)
    + '&wpStarttime=' + encodeURIComponent(wpStarttime)
    + '&wpEdittime=' + encodeURIComponent(wpEdittime)
    + '&wpEditToken=' + encodeURIComponent(wpEditToken)
    + '&wpSummary=' + encodeURIComponent('[[Discussion_utilisateur:Arkanosis/xpatrol.js|xpatrol]] : ' + reason);

  if (xpatrolWatchOthers || xpatrolWatchMain && !wgNamespaceNumber)
    parameters += '&wpWatchthis=on';

  request.open('POST', wgServer + wgScriptPath + '/index.php?title=' + encodeURIComponent(article) + '&action=submit', true);

  request.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
  request.setRequestHeader('Content-length', parameters.length);
  request.setRequestHeader('Connection', 'close');

  request.send(parameters);

  // TODO reload the page content instead (another AJAX request)
  if (!text)
    document.getElementById('content').removeChild(document.getElementById('bodyContent'));

  if (button)
  {
    link = document.getElementById(button);
    link.innerHTML = '<img src="http://upload.wikimedia.org/wikipedia/commons/thumb/f/fb/Yes_check.svg/15px-Yes_check.svg.png" /> ' + link.innerHTML
  }
}

function xpatrolClear(article, reason, button)
{
  if (!confirm('Blanchir l\'article ' + article + ' pour ' + reason + ' ?'))
    return;

  xpatrolEdit(article, '', reason, button);
}

function xpatrolAddBanner(article, banner, reason, button)
{
  if (!confirm('Ajouter le bandeau ' + banner + ' à l\'article ' + article + ' pour ' + reason + ' ?'))
    return;

  xpatrolEdit(article, '{{' + banner + '}}\n\n$$text$$', reason, button);
}

function xpatrolAddCheckLinks(tag)
{
  var elts = document.getElementsByTagName(tag);
  for (var eltId = 0; eltId < elts.length; ++eltId)
    if (elts[eltId].className == 'patrollink')
    {
      var link = elts[eltId].childNodes[1];
      url = link.getAttribute('href');
      link.setAttribute('href', 'javascript:xpatrolCheck("' + url + '", "' + tag + '");');
      break;
    }
}

function xpatrolAddHistoryLinks()
{

}

function xpatrolAddNewPagesLinks()
{
  var tds = document.getElementsByTagName('td');
  for (var tdId = 0; tdId < tds.length; ++tdId)
    if (tds[tdId].className == 'mw-input')
    {
      tds[tdId].innerHTML = tds[tdId].innerHTML.replace('</a> les redirections', '</a> les redirections | <a id="xpatrol-ToggleEmptyNewPages" href="javascript:xpatrolToggleEmptyNewPages();" title="Spécial:Nouvelles pages">masquer</a> les pages blanchies');
    }
}

function xpatrolAddClearLink(label, hint, message)
{
  var body = document.getElementById('bodyContent');

  var link = document.createElement('a');
  link.setAttribute('href', 'javascript:xpatrolClear("' + wgPageName + '", "' + message + '", "xpatrol-' + label + '");');
  link.setAttribute('id', 'xpatrol-' + label);
  link.setAttribute('title', hint);
  link.appendChild(document.createTextNode(' ' + label + ' '));

  document.getElementById('content').insertBefore(link, body);
}

function xpatrolAddClearLinks()
{
  xpatrolAddClearLink('BàS', 'Bac à sable', '[[Wikipédia:Bac à sable|Bac à sable]]');
  xpatrolAddClearLink('HC', 'Hors critères d\'admissibilité des articles', '[[WP:CAA|Critères d\'admissibilité non atteints]]');
  xpatrolAddClearLink('NEEE', 'Non encyclopédique en l\'état', 'Non encyclopédique en l\'état');
  xpatrolAddClearLink('Promo', 'Contenu à caractère promotionnel', 'Contenu à caractère promotionnel');
  xpatrolAddClearLink('Spam', 'Spam et / ou liens externes non appropriés', 'Spam');
  xpatrolAddClearLink('Diffm', 'Diffamation', 'Diffamation');
  xpatrolAddClearLink('Copie', 'Copie d\'un article existant de Wikipédia', 'Copie de l\'article [[" + prompt("Quel est l\'article de Wikipédia copié ?", "") + "]]');
  xpatrolAddClearLink('Cpvio', 'Violation des droits d\'auteur', 'Violation des droits d\'auteur (" + prompt("Quelle est la source copiée illégalement ?", "") + ")');
}

function xpatrolAddBannerLink(label, hint, banner, message)
{
  var body = document.getElementById('bodyContent');

  var link = document.createElement('a');
  link.setAttribute('href', 'javascript:xpatrolAddBanner("' + wgPageName + '", "' + banner + '", "' + message + '", "xpatrol-' + label + '");');
  link.setAttribute('id', 'xpatrol-' + label);
  link.setAttribute('title', hint);
  link.appendChild(document.createTextNode(' ' + label + ' '));

  document.getElementById('content').insertBefore(link, body);
}

function xpatrolAddBannerLinks()
{
  var today = new Date();

  xpatrolAddBannerLink('?', 'Incompréhensible dans l’état actuel', '?', '[[WP:RI|Incompréhensible dans l\’état actuel]]');
  xpatrolAddBannerLink('Pub', 'Ton trop promotionnel ou publicitaire', 'pub', '[[WP:POV|Ton trop promotionnel ou publicitaire]]');
  xpatrolAddBannerLink('Admi', 'Admissibilité à vérifier', 'admissibilité|date={{date|' + today.getDate() + '|' + month(today.getMonth()) + '|' + (1900 + today.getYear()) + '}}', '[[WP:CAA|Admissibilité à vérifier]]');
  xpatrolAddBannerLink('Orth', 'Orthographe et grammaire à vérifier', 'Orthographe', 'Orthographe et grammaire à vérifier');
  xpatrolAddBannerLink('Redac', 'Style non encyclopédique', 'Rédaction', '[[WP:STYLE|Style non encyclopédique]]');
}

function xpatrolAddAbuseFilterLinks()
{
  var link = new RegExp('(sur <a href="/wiki/([^"]+)" title="[^"]+">[^<]+</a>)(\.\nActions prises)');

  if (location.href.indexOf('&details=') != -1)
    var lis = document.getElementsByTagName('p');
  else
    var lis = document.getElementsByTagName('li');

  for (var liId = 0; liId < lis.length; ++liId)
  {
    var match = link.exec(lis[liId].innerHTML);
    if (match)
      lis[liId].innerHTML = lis[liId].innerHTML.replace(match[0], match[1] + ' (<a href="' + wgServer + wgScript + '?title=' + match[2] + '&action=history" title="historique">h</a> · <a href="' + wgServer + wgScript + '?title=Spécial:Log&page=' + match[2] + '" title="journaux">j</a>)' + match[3]);
  }
}

function xpatrol()
{
  if (location.href.indexOf('&diff') != -1)
    xpatrolAddCheckLinks('span');
  else if (location.href.indexOf('&action=history') != -1)
    xpatrolAddHistoryLinks();
  else if (wgPageName == 'Spécial:Nouvelles_pages')
    xpatrolAddNewPagesLinks();
  else if (wgPageName == 'Spécial:Journal_du_filtre_antiabus')
    xpatrolAddAbuseFilterLinks();
  else
  {
    if (location.href.indexOf('&rcid') != -1)
      xpatrolAddCheckLinks('div');
    if (document.getElementById('ca-edit'))
    {
      if (xpatrolEnableClear && wgUserGroups.indexOf('autoconfirmed') != -1)
        xpatrolAddClearLinks();
      if (xpatrolEnableBanner)
        xpatrolAddBannerLinks();
    }
  }
}

addOnloadHook(xpatrol);