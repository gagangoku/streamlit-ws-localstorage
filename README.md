# streamlit-ws-localstorage
Finally a simple synchronous way of accessing localStorage from your Streamlit app.

# Why
I tried using extra-streamlit-components but found it too complex, because of the way Streamlit components works.
Since the communication between the browser and streamlit app is async, your app is run multiple times, and nested if else blocks may not work properly. A simple call to get all cookies causes the app to be run 4 times in total. And the first call to get all cookies returns an empty dictionary which needs to be handled in the code.

Looking at the complexity, I thought it would be easier to write a synchronous commmunication.


# How to run
Using it is fairly simple:


```python
import streamlit as st
from streamlit_ws_localstorage import injectWebsocketCode, getOrCreateUID

# Main call to the api, returns a communication object
conn = injectWebsocketCode(hostPort='linode.liquidco.in', uid=getOrCreateUID())

st.write('setting into localStorage')
ret = conn.setLocalStorageVal(key='k1', val='v1')
st.write('ret: ' + ret)

st.write('getting from localStorage')
ret = conn.getLocalStorageVal(key='k1')
st.write('ret: ' + ret)
```

You can use the ```linode.liquidco.in``` websocket relay server for testing. Alternately run your websocket relay server from the code in ```websocket-server/ws_server.py```

# Video demo
https://user-images.githubusercontent.com/544881/185042658-43dd3c58-a086-4457-a042-9d4d895e34ba.mp4

