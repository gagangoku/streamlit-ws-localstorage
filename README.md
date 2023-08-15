# streamlit-ws-localstorage
Finally a simple synchronous way of accessing localStorage from your Streamlit app.

[![Downloads](https://static.pepy.tech/personalized-badge/streamlit-ws-localstorage?period=total&units=international_system&left_color=black&right_color=orange&left_text=Downloads)](https://pepy.tech/project/streamlit-ws-localstorage)

# Why
I wanted to include a login with Google / Linkedin button on my Streamlit app. Tried many modules but didn’t get the experience I wanted.

I tried using extra-streamlit-components but found it too complex, because of the way Streamlit components works.
Since the communication between the browser and streamlit app is async, your app is run multiple times, and nested if else blocks may not work properly. A simple call to get all cookies causes the app to be run 4 times in total. And the first call to get all cookies returns an empty dictionary which needs to be handled in the code.

Looking at the complexity, I thought it would be easier to write a synchronous commmunication.


# How to run
Using it is fairly simple:


```python
import streamlit as st
import uuid
from streamlit_ws_localstorage import injectWebsocketCode

# You can use my server for now, or run your own websocket server and auth redirect servers from here:
# https://github.com/gagangoku/streamlit-ws-localstorage/tree/main/streamlit_ws_localstorage
HOST_PORT = 'wsauthserver.supergroup.ai'

# Main call to the api, returns a communication object
conn = injectWebsocketCode(hostPort=HOST_PORT, uid=str(uuid.uuid1()))

st.write('setting into localStorage')
ret = conn.setLocalStorageVal(key='k1', val='v1')
st.write('ret: ' + ret)

st.write('getting from localStorage')
ret = conn.getLocalStorageVal(key='k1')
st.write('ret: ' + ret)
```

You can use the ```wsauthserver.supergroup.ai``` websocket relay server for testing. Alternately run your websocket relay server from the code in ```websocket-server/ws_server.py```


# Oauth
I’ve also built a Linkedin Oauth example using the same:

```python
import uuid

import streamlit as st
import streamlit.components.v1 as components
from linkedin_v2 import linkedin
from streamlit_ws_localstorage import injectWebsocketCode
from streamlit_ws_localstorage.auth_redirect_server.auth_util import loginWithOAuthComponent


USER_PROFILE_PIC_KEY = '_user.profilePic'
USER_EMAIL_ADDRESS_KEY = '_user.emailAddress'
AUTH_CODE_KEY = '_linkedin.authCode'

# You can use my server for now, or run your own websocket server and auth redirect servers from here:
# https://github.com/gagangoku/streamlit-ws-localstorage/tree/main/streamlit_ws_localstorage
HOST_PORT = 'wsauthserver.supergroup.ai'

# Use this to avoid handling redirects in your app.
# Don't forget to register this as a redirect url in your linkedin app.
REDIRECT_URL = 'https://authredirect.supergroup.in/redirect'


def getLinkedinOauth(uid):
    CLIENT_KEY = '<your client key>'
    CLIENT_SECRET = '<your client secret>'
    authentication = linkedin.LinkedInAuthentication(CLIENT_KEY, CLIENT_SECRET, REDIRECT_URL,
                                                     ['r_liteprofile', 'r_emailaddress'])

    # Set the state variable as the uid so the browser can receive the auth code corresponding to this request
    authentication.state = uid
    return authentication


def getLinkedinUserProfile(code):
    authObj = getLinkedinOauth('')
    authObj.authorization_code = code
    authToken = authObj.get_access_token()

    application = linkedin.LinkedInApplication(token=authToken)
    profile = application.get_profile()
    print('profile: ', profile)
    firstName, lastName, displayImage, id = profile['localizedFirstName'], profile['localizedLastName'], profile['profilePicture']['displayImage'], profile['id']

    # Get profile picture
    response = application.make_request('GET', 'https://api.linkedin.com/v2/me?projection=(profilePicture(displayImage~:playableStreams))')
    json_response = response.json()
    print ('profile pic json_response: ', json_response)
    profilePic = json_response['profilePicture']['displayImage~']['elements'][2]['identifiers'][0]['identifier']

    # Get email
    response = application.make_request('GET', 'https://api.linkedin.com/v2/emailAddress?q=members&projection=(elements*(handle~))')
    json_response = response.json()
    print ('email json_response: ', json_response)
    emailAddress = json_response['elements'][0]['handle~']['emailAddress']

    rsp = (firstName, lastName, displayImage, id, profilePic, emailAddress)
    print ('getLinkedinUserProfile: ', rsp)
    return rsp


def logoutFn():
    conn = injectWebsocketCode(hostPort=HOST_PORT, uid=str(uuid.uuid1()))
    conn.setLocalStorageVal(key=USER_PROFILE_PIC_KEY, val='')
    conn.setLocalStorageVal(key=USER_EMAIL_ADDRESS_KEY, val='')
    conn.setLocalStorageVal(key=AUTH_CODE_KEY, val='')
    st.write('Logged out, reloading the page')
    code = """<script>setTimeout(() => window.parent.location.reload(), 1000)</script>"""
    components.html(code, height=100)


def main():
    st.title('Login demo')

    uid = str(uuid.uuid1())
    conn = injectWebsocketCode(hostPort=HOST_PORT, uid=uid)
    print('conn: ', conn)

    emailAddress = conn.getLocalStorageVal(key=USER_EMAIL_ADDRESS_KEY)
    authCode = conn.getLocalStorageVal(key=AUTH_CODE_KEY)
    if authCode and not emailAddress:
        (firstName, lastName, displayImage, id, profilePic, emailAddress) = getLinkedinUserProfile(authCode)
        conn.setLocalStorageVal(key=USER_PROFILE_PIC_KEY, val=profilePic)
        conn.setLocalStorageVal(key=USER_EMAIL_ADDRESS_KEY, val=emailAddress)

    profilePic = conn.getLocalStorageVal(key=USER_PROFILE_PIC_KEY)
    emailAddress = conn.getLocalStorageVal(key=USER_EMAIL_ADDRESS_KEY)
    if emailAddress:
        st.write('Welcome ' + emailAddress)
        st.image(profilePic, width=200)
        st.button('Logout', on_click=logoutFn)
    else:
        uid = str(uuid.uuid1())
        authObj = getLinkedinOauth(uid)
        st.markdown('<a href="{}" target="_blank">Login with LinkedIn</a>'.format(authObj.authorization_url), unsafe_allow_html=True)
        loginWithOAuthComponent(HOST_PORT, uid, AUTH_CODE_KEY, reloadInSecs=6, height=40)


main()
```

This shows a `Login with LinkedIn` link which opens the Linkedin auth page in a new tab, which upon success redirects to https://authredirect.supergroup.in/redirect. You can use this to avoid handling page redirects in your streamlit app.

If there’s interest, I can make simple button components for Linkedin, Google, Github to simplify this even further.



# Video demo of localstorage
https://user-images.githubusercontent.com/544881/185042658-43dd3c58-a086-4457-a042-9d4d895e34ba.mp4

# Video demo of oauth login with linkedin
https://user-images.githubusercontent.com/544881/185403846-959c6c2c-493d-41e7-bcc0-665721f3cb13.mp4


# Installation

Installation: `pip install streamlit-ws-localstorage`

Repository: [GitHub - gagangoku/streamlit-ws-localstorage: A simple synchronous way of accessing localStorage from your Streamlit app. ](https://github.com/gagangoku/streamlit-ws-localstorage)

On pypi: [streamlit-ws-localstorage · PyPI](https://pypi.org/project/streamlit-ws-localstorage/)
