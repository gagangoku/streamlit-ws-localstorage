# python -u to disable buffering
# https://stackoverflow.com/questions/43197518/print-statements-not-working-when-serve-forever-is-called/43304567#43304567

# Run websocket server
nohup ./venv/bin/python3 -u streamlit_ws_localstorage/websocket-server/ws_server.py 2>&1 > logs/ws-$(date '+%Y-%m-%dT%H:%M:%S').log &

# Run auth redirect server
nohup ./venv/bin/python3 -u streamlit_ws_localstorage/auth-redirect-server/auth_redirect_server.py 2>&1 > logs/auth-$(date '+%Y-%m-%dT%H:%M:%S').log &

