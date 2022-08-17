import asyncio
import json
import ssl
import time
import uuid

import certifi
import streamlit as st
import streamlit.components.v1 as components
import websockets


def getOrCreateUID():
    if 'uid' not in st.session_state:
        st.session_state['uid'] = ''
    st.session_state['uid'] = st.session_state['uid'] or str(uuid.uuid1())
    print ('getOrCreateUID: ', st.session_state['uid'])
    return st.session_state['uid']


# Generate a unique uid that gets embedded in components.html for frontend
# Both frontend and server connect to ws using the same uid
# server sends commands like localStorage_get_key, localStorage_set_key, localStorage_clear_key etc. to the WS server,
# which relays the commands to the other connected endpoint (the frontend), and back
def injectWebsocketCode(hostPort, uid):
    code = '<script>function connect() { console.log("in connect uid: ", "' + uid + '"); var ws = new WebSocket("wss://' + hostPort + '/?uid=' + uid + '");' + """
  ws.onopen = function() {
    // subscribe to some channels
    // ws.send(JSON.stringify({ status: 'connected' }));
    console.log("onopen");
  };

  ws.onmessage = function(e) {
    console.log('Message:', e.data);
    var obj = JSON.parse(e.data);
    if (obj.cmd == 'localStorage_get_key') {
        var val = localStorage[obj.key] || '';
        ws.send(JSON.stringify({ status: 'success', val }));
        console.log('returning: ', val);
    } else if (obj.cmd == 'localStorage_set_key') {
        localStorage[obj.key] = obj.val;
        ws.send(JSON.stringify({ status: 'success' }));
        console.log('set: ', obj.key, obj.val);
    }
  };

  ws.onclose = function(e) {
    console.log('Socket is closed. Reconnect will be attempted in 1 second.', e.reason);
    setTimeout(function() {
      connect();
    }, 1000);
  };

  ws.onerror = function(err) {
    console.error('Socket encountered error: ', err.message, 'Closing socket');
    ws.close();
  };
}

connect();
</script>
        """
    components.html(code, height=0)
    time.sleep(1)       # Without sleep there are problems
    return WebsocketClient(hostPort, uid)


class WebsocketClient:
    def __init__(self, hostPort, uid):
        self.hostPort = hostPort
        self.uid = uid
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

    def sendCommand(self, value, waitForResponse=True):
        ssl_context = ssl.create_default_context()
        ssl_context.load_verify_locations(certifi.where())

        async def query(future):
            async with websockets.connect("wss://" + self.hostPort + "/?uid=" + self.uid, ssl=ssl_context) as ws:
                await ws.send(value)
                if waitForResponse:
                    response = await ws.recv()
                    print('response: ', response)
                    future.set_result(response)
                else:
                    future.set_result('')

        future1 = asyncio.Future()
        self.loop.run_until_complete(query(future1))
        print('future1.result: ', future1.result())
        return future1.result()

    def getLocalStorageVal(self, key):
        result = self.sendCommand(json.dumps({ 'cmd': 'localStorage_get_key', 'key': key }))
        return json.loads(result)['val']

    def setLocalStorageVal(self, key, val):
        result = self.sendCommand(json.dumps({ 'cmd': 'localStorage_set_key', 'key': key, 'val': val }))
        return result

