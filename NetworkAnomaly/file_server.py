import os
from http.server import HTTPServer, SimpleHTTPRequestHandler
import socketserver
import json
import threading
import webbrowser

class CORSRequestHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        # Enable CORS
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def do_GET(self):
        if self.path == '/api/latest-report':
            try:
                # Path to reports directory
                reports_dir = os.path.join(os.path.dirname(__file__), 'reports')
                
                # Get all JSON files in the reports directory
                reports = [
                    os.path.join(reports_dir, f) 
                    for f in os.listdir(reports_dir) 
                    if f.endswith('.json')
                ]
                
                # Find the most recent report
                if not reports:
                    self.send_response(404)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({"error": "No reports found"}).encode())
                    return
                
                latest_report = max(reports, key=os.path.getctime)
                
                # Read the latest report
                with open(latest_report, 'r') as f:
                    report_data = json.load(f)
                
                # Send the report
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(report_data).encode())
            
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode())
        else:
            # Serve files from the current directory
            super().do_GET()

def start_file_server(port=8000):
    # Ensure reports directory exists
    reports_dir = os.path.join(os.path.dirname(__file__), 'reports')
    os.makedirs(reports_dir, exist_ok=True)
    
    # Change working directory to project root
    os.chdir(os.path.dirname(__file__))
    
    # Start the server
    with socketserver.TCPServer(("", port), CORSRequestHandler) as httpd:
        print(f"Serving at http://localhost:{port}")
        print("Press Ctrl+C to stop the server")
        httpd.serve_forever()

def main():
    start_file_server()

if __name__ == "__main__":
    main()