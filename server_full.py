#!/usr/bin/env python3
"""
Tâm Việt Quang - Full HTTP Server with POST support
Port: 3960 (HTML) + 3961 (API)
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import os
from datetime import datetime
import re

# ===== CONFIG =====
HTML_PORT = 3960
API_PORT = 3961
DATA_DIR = 'data'
CONTACTS_FILE = os.path.join(DATA_DIR, 'contacts.json')

# ===== DATABASE =====
os.makedirs(DATA_DIR, exist_ok=True)
if not os.path.exists(CONTACTS_FILE):
    with open(CONTACTS_FILE, 'w', encoding='utf-8') as f:
        json.dump([], f)

def load_contacts():
    try:
        with open(CONTACTS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []

def save_contacts(contacts):
    with open(CONTACTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(contacts, f, indent=2, ensure_ascii=False)

# ===== HTML SERVER =====
class HTMLHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Serve index.html for root
        if self.path == '/':
            self.path = '/index.html'
        
        # Try to serve file
        try:
            file_path = self.path.lstrip('/')
            if os.path.exists(file_path) and os.path.isfile(file_path):
                with open(file_path, 'rb') as f:
                    content = f.read()
                
                # Determine content type
                if file_path.endswith('.html'):
                    content_type = 'text/html; charset=utf-8'
                elif file_path.endswith('.css'):
                    content_type = 'text/css; charset=utf-8'
                elif file_path.endswith('.js'):
                    content_type = 'application/javascript; charset=utf-8'
                elif file_path.endswith('.png'):
                    content_type = 'image/png'
                elif file_path.endswith('.jpg') or file_path.endswith('.jpeg'):
                    content_type = 'image/jpeg'
                else:
                    content_type = 'application/octet-stream'
                
                self.send_response(200)
                self.send_header('Content-Type', content_type)
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(content)
            else:
                self.send_error(404, 'File not found')
        except Exception as e:
            self.send_error(500, str(e))
    
    def log_message(self, format, *args):
        print(f"📄 {self.address_string()} - {args[0]}")

# ===== API SERVER =====
class APIHandler(BaseHTTPRequestHandler):
    def send_json(self, status, data):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))
    
    def do_OPTIONS(self):
        self.send_json(200, {'status': 'ok'})
    
    def do_GET(self):
        if self.path == '/api/contacts':
            contacts = load_contacts()
            self.send_json(200, {
                'success': True,
                'count': len(contacts),
                'data': contacts
            })
            print(f"✅ GET /api/contacts - {len(contacts)} contacts")
        else:
            self.send_json(404, {'success': False, 'message': 'Not found'})
    
    def do_POST(self):
        if self.path == '/api/contacts':
            try:
                content_length = int(self.headers.get('Content-Length', 0))
                body = self.rfile.read(content_length).decode('utf-8')
                data = json.loads(body)
                
                # Validate
                name = data.get('name', '').strip()
                email = data.get('email', '').strip()
                company = data.get('company', '').strip()
                message = data.get('message', '').strip()
                
                if not name or not email or not message:
                    self.send_json(400, {
                        'success': False,
                        'message': 'Vui lòng điền đầy đủ thông tin'
                    })
                    return
                
                # Create contact
                new_contact = {
                    'id': str(int(datetime.now().timestamp() * 1000)),
                    'name': name,
                    'email': email,
                    'company': company,
                    'message': message,
                    'timestamp': datetime.now().isoformat(),
                    'status': 'new'
                }
                
                # Save
                contacts = load_contacts()
                contacts.append(new_contact)
                save_contacts(contacts)
                
                print(f"✅ POST /api/contacts - Saved: {name} <{email}>")
                
                self.send_json(201, {
                    'success': True,
                    'message': 'Gửi thành công!',
                    'data': new_contact
                })
                
            except Exception as e:
                print(f"❌ Error: {e}")
                self.send_json(500, {
                    'success': False,
                    'message': 'Có lỗi xảy ra',
                    'error': str(e)
                })
        else:
            self.send_json(404, {'success': False, 'message': 'Not found'})
    
    def log_message(self, format, *args):
        pass

# ===== MAIN =====
def run_html_server():
    server = HTTPServer(('', HTML_PORT), HTMLHandler)
    print(f'🌐 HTML Server: http://localhost:{HTML_PORT}')
    server.serve_forever()

def run_api_server():
    server = HTTPServer(('', API_PORT), APIHandler)
    print(f'📧 API Server: http://localhost:{API_PORT}/api/contacts')
    server.serve_forever()

if __name__ == '__main__':
    import threading
    
    print('🚀 Tâm Việt Quang Server')
    print('=' * 50)
    
    # Run both servers
    html_thread = threading.Thread(target=run_html_server, daemon=True)
    api_thread = threading.Thread(target=run_api_server, daemon=True)
    
    html_thread.start()
    api_thread.start()
    
    print(f'📁 Data: {CONTACTS_FILE}')
    print('Press Ctrl+C to stop')
    print()
    
    try:
        html_thread.join()
        api_thread.join()
    except KeyboardInterrupt:
        print('\n👋 Stopped')
