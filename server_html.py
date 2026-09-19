#!/usr/bin/env python3
"""
Tâm Việt Quang - Static HTML Server
Chạy trên port 3960
"""

from http.server import HTTPServer, SimpleHTTPRequestHandler
import os

class StaticHandler(SimpleHTTPRequestHandler):
    """Handler cho static files"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory='.', **kwargs)
    
    def end_headers(self):
        """Thêm CORS headers"""
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        super().end_headers()
    
    def do_OPTIONS(self):
        """Handle OPTIONS request (CORS preflight)"""
        self.send_response(200)
        self.end_headers()
    
    def log_message(self, format, *args):
        """Custom log message"""
        print(f"📄 {self.address_string()} - {format % args}")

def main():
    """Chạy server"""
    port = 3960
    
    # Chuyển đến thư mục website
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    server = HTTPServer(('', port), StaticHandler)
    
    print('🌐 Tâm Việt Quang HTML Server Started')
    print(f'📍 Website: http://localhost:{port}')
    print(f'📁 Serving from: {script_dir}')
    print('Press Ctrl+C to stop the server')
    print()
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\n\n👋 Server stopped')
        server.shutdown()

if __name__ == '__main__':
    main()
