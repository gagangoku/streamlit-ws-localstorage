import time

import streamlit.components.v1 as components


def loginWithOAuthComponent(hostPort, uid, localStorageCodeKey, reloadInSecs=5, height=40):
    code = """<div id="statusDiv">Waiting for auth code</div>
<script>
function connect(hostPort, uid, localStorageCodeKey, reloadInSecs) {
  console.log("in loginWithOAuthComponent connect uid: ", uid);
  var ws = new WebSocket("wss://" + hostPort + "/?uid=" + uid);
  ws.onopen = function() {
    // subscribe to some channels
    console.log("loginWithOAuthComponent onopen");
  };

  ws.onmessage = function(e) {
    console.log('loginWithOAuthComponent onmessage:', e.data);
    var obj = JSON.parse(e.data);
    if (obj.cmd == 'process_auth_redirect') {
        console.log('process_auth_redirect: ', obj);
        var code = obj['code'];
        localStorage[localStorageCodeKey] = code;
        console.log('saving code: ', code);

        var div = document.getElementById("statusDiv");
        div.innerHTML = 'Auth code received. Reloading page in ' + reloadInSecs + ' seconds';
        setTimeout(() => window.parent.location.reload(), reloadInSecs*1000);
    }
  };

  ws.onclose = function(e) {
    console.log('loginWithOAuthComponent onclose: Socket is closed. Reconnect will be attempted in 1 second.', e.reason);
    setTimeout(function() {
      connect();
    }, 1000);
  };

  ws.onerror = function(err) {
    console.error('loginWithOAuthComponent onerror: Socket encountered error: ', err.message, 'Closing socket');
    ws.close();
  };
}""" + "connect('{}', '{}', '{}', {});</script>".format(hostPort, uid, localStorageCodeKey, reloadInSecs)
    components.html(code, height=height)
    time.sleep(1)
