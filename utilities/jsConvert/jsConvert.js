function $(id)
{
  return document.getElementById(id);
}

function test()
{
  var result = $('result');
  var analysis = $('analysis');
  var replacement = $('replacement');
  var wgServer = 'http://fr.wikipedia.org';

  var regexp = new RegExp($('regexp').value, $('flags').value);
  if (replacement.value)
  {
    analysis.innerHTML = '<span class="plainlinks">' + $('text').value
      .split(' (<span class="mw-history-undo">')[0]
      .replace(new RegExp('<input type="radio"[^>]*?/>', 'g'), '')
      .replace(new RegExp('<a href="/wiki/([^"]+)"[^>]*?>(.+?)</a>', 'g'), '[[$1|$2]]')
      .replace(new RegExp('<a href="/w/index\\.php\\?title=([^"]+)redlink=1"[^>]*?>(.+?)</a>', 'g'), '[[$1|$2]]')
      .replace(new RegExp('<a href="(/w/index\\.php\\?title=[^"]+)"[^>]*?>(.+?)</a>', 'g'), '[' + wgServer + '$1 $2]')
      + '</span>';
    //result.innerHTML = 'REPLACEMENT: <code>' + $('text').value.replace(regexp, replacement.value) + '</code>';
  }
  else
  {
    var results = regexp.exec($('text').value);
    if (results)
    {
      result.innerHTML = 'OK: <code>' + results + '</code>';
      var list = '<ol>';
      for (var groupId = 1; groupId < results.length; ++groupId)
      {
	list += '<li>' + results[groupId] + '</li>';
      }
      analysis.innerHTML = list + '</ol>';
    }
    else
    {
      result.innerHTML = 'KO';
    }
  }
}

// <a href="/wiki/([^"]+)"[^>]*>(.+?)</a>"
// <a href="/w/index.php\?title=([^"]+)"[^>]*>(.+?)</a>"
// [[$1|$2]]