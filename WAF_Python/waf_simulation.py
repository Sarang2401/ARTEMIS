from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse

class WAFHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('input.html', 'rb') as file:
                self.wfile.write(file.read())
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == '/process':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            parsed_data = urllib.parse.parse_qs(post_data)
            user_input = parsed_data.get('user_input', [''])[0]

            if self.is_sql_injection(user_input) or self.is_xss(user_input):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b'<h1>Blocked! Malicious input detected.</h1>')
            else:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(f'<h1>Input Received: {user_input}</h1>'.encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

    def is_sql_injection(self, input_string):
        sql_keywords = ['SELECT', 'INSERT', 'UPDATE', 'DELETE', 'UNION']
        for keyword in sql_keywords:
            if keyword.lower() in input_string.lower():
                return True
        return False

    def is_xss(self, input_string):
        xss_patterns = ['<script>', 'javascript:']
        for pattern in xss_patterns:
            if pattern.lower() in input_string.lower():
                return True
        return False

def run(server_class=HTTPServer, handler_class=WAFHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()