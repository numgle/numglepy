from http.server import BaseHTTPRequestHandler, HTTPServer
import numgle

port = 3001

class BasicHTTPReqHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        param = self.path.split("/")[-1]
        numglefied = numgle.numglefy(param)
        self.wfile.write(numglefied.encode())

httpd = HTTPServer(('0.0.0.0', port), BasicHTTPReqHandler)
httpd.serve_forever()