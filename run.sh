#!/bin/bash

set -x
set -e

# Run websocket server
PYTHONPATH=. python -u streamlit_ws_localstorage/websocket_server/ws_server.py &

# Run auth redirect server
PYTHONPATH=. python -u streamlit_ws_localstorage/auth_redirect_server/auth_redirect_server.py
