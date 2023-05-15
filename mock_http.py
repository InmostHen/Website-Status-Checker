import http.server
import socketserver

PORT = 8000

class MockServerRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"Hello, World!")
        else:
            self.send_error(500, 'Website is down')


with socketserver.TCPServer(("", PORT), MockServerRequestHandler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()
