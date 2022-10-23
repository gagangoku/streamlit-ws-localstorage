#!/bin/bash

set -x
set -e

# Linode
rsync -r -avzh --exclude 'build' --exclude 'dist' --exclude 'streamlit_ws_localstorage.egg-info' --exclude '.git' ../streamlit-ws-localstorage/ gagan@ezinvest.in:~/streamlit-ws-localstorage/

# Gcp
rsync -Pa -e "ssh -t -i /Users/gagandeep/.ssh/google_compute_engine -o CheckHostIP=no -o HashKnownHosts=no -o HostKeyAlias=compute.8593189175368638566 -o IdentitiesOnly=yes -o StrictHostKeyChecking=yes -o UserKnownHostsFile=/Users/gagandeep/.ssh/google_compute_known_hosts" --exclude venv --exclude .git ./ gagandeep@gcp.liquidco.in:~/streamlit-ws-localstorage/
