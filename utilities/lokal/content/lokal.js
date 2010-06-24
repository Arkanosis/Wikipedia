var Lokal =
{
  init: function()
  {
    var appcontent = document.getElementById("appcontent");

    this.io = Components.classes["@mozilla.org/network/io-service;1"].getService(Components.interfaces.nsIIOService),

    this.resource = this.io.getProtocolHandler("resource").QueryInterface(Components.interfaces.nsIResProtocolHandler),
    this.resource.setSubstitution('lokal', this.io.newURI("chrome:lokal/content/", null, null));

    this.observer = Components.classes["@mozilla.org/observer-service;1"].getService(Components.interfaces.nsIObserverService),
    this.observer.addObserver(Lokal, "http-on-modify-request", false);
  },

  destroy: function()
  {
    this.observer.removeObserver(LocalLoad, "http-on-modify-request");
  },

  getBrowserFromChannel: function (aChannel) {
    try {
      var notificationCallbacks = aChannel.notificationCallbacks ? aChannel.notificationCallbacks : aChannel.loadGroup.notificationCallbacks;

      if (!notificationCallbacks) {
	return null;
      }

      var domWin = notificationCallbacks.getInterface(Components.interfaces.nsIDOMWindow);
      return gBrowser.getBrowserForDocument(domWin.top.document);
    } catch (e) {
      return null;
    }
  },

  observe: function(subject, topic, data)
  {
    subject.QueryInterface(Components.interfaces.nsIHttpChannel);
    var url = subject.URI.spec;

    if (url.indexOf('xpatrol') != -1)
    {
//       var browser = this.getBrowserFromChannel(subject);
//       if (browser != null)
//       {
      var script = browser.contentDocument.querySelectorAll('script[hookable=true]')[0];
      subject.cancel(Components.results.NS_ERROR_ABORT);
      var s = script.ownerDocument.createElement('script');
      s.src = 'resource://lokal/xpatrol.js';
      script.parentNode.replaceChild(s, script);
//       }
    }
  },

};

window.addEventListener("load", Lokal.init, false);
window.addEventListener("unload", Lokal.destroy, false);
