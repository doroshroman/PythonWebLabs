from http.server import HTTPServer, CGIHTTPRequestHandler

PORT = 8000
server_address = ("", PORT)
httpd = HTTPServer(server_address, CGIHTTPRequestHandler)
httpd.serve_forever()