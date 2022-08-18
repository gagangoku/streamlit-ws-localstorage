import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import logging

from streamlit_ws_localstorage import WebsocketClient

hostName = "0.0.0.0"
serverPort = 8002


# Server to handle /redirect urls that come from OAuth 2 redirects
# Upon receiving the code and state variables from the request, sends it to the Websocket server with the state as uid
# The auth initiator should be listening to the websocket server using same the uid, thus it can receive the code
class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            parsed_url = urlparse(self.path)
            d = parse_qs(parsed_url.query)
            if parsed_url.path == '/redirect' and 'code' in d and 'state' in d:
                # Validation passed
                code = d['code'][0]
                state = d['state'][0]
                closeTab = 'closeTab' in d and d['closeTab'][0].lower() == 'true'
                logging.info('code, state, closeTab: {} {} {}'.format(code, state, str(closeTab)))
                conn = WebsocketClient('linode.liquidco.in', state)
                ret = conn.sendCommand(json.dumps({ 'cmd': 'process_auth_redirect', 'code': code, 'state': state }), waitForResponse=False)
                ret = 'AUTH SUCCESS ' + ret
                self.sendText(ret, closeTab=closeTab)
            else:
                # Validation failed
                self.sendText('AUTH FAILED: Bad url', status=400)
        except Exception:
            self.sendText('AUTH FAILED: Exception', status=502)
            logging.exception("Exception")

    def sendText(self, text, status=200, closeTab=False):
        self.send_response(status)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        script = '<div style="font-size: 14px; margin-top: 10px;">This tab will automatically close soon. If it doesnt, please close it manually.</div><script>setTimeout(() => window.close(), 2000);</script>' if closeTab else ''
        html = '<html><head><title>Auth redirect server</title></head><body><div style="font-size: 20px; margin-top: 10px;">{}</div>{}</body></html>'.format(text, script)
        self.wfile.write(bytes(html, "utf-8"))


if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
