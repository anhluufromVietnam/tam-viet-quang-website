#!/usr/bin/env python3
"""
Tâm Việt Quang - Single Server
HTML + API trên cùng 1 port
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import os
from datetime import datetime
import mimetypes

# ===== CONFIG =====
PORT = 3960
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

# ===== HANDLER =====
class Handler(BaseHTTPRequestHandler):
    
    def send_json(self, status, data):
        """Gửi JSON response"""
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))
    
    def send_file(self, file_path):
        """Gửi file"""
        try:
            with open(file_path, 'rb') as f:
                content = f.read()
            
            # Determine content type
            content_type, _ = mimetypes.guess_type(file_path)
            if content_type is None:
                if file_path.endswith('.html'):
                    content_type = 'text/html; charset=utf-8'
                elif file_path.endswith('.css'):
                    content_type = 'text/css; charset=utf-8'
                elif file_path.endswith('.js'):
                    content_type = 'application/javascript; charset=utf-8'
                else:
                    content_type = 'application/octet-stream'
            
            self.send_response(200)
            self.send_header('Content-Type', content_type)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(content)
            
        except FileNotFoundError:
            self.send_error(404, 'File not found')
        except Exception as e:
            self.send_error(500, str(e))
    
    def do_OPTIONS(self):
        """Handle CORS preflight"""
        self.send_json(200, {'status': 'ok'})
    
    def do_GET(self):
        """Handle GET requests"""
        
        # API: Get contacts
        if self.path == '/api/contacts':
            contacts = load_contacts()
            self.send_json(200, {
                'success': True,
                'count': len(contacts),
                'data': contacts
            })
            print(f"✅ GET /api/contacts - {len(contacts)} contacts")
            return
        
        # API: Export contacts
        if self.path == '/api/contacts/export':
            contacts = load_contacts()
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Disposition', 'attachment; filename=contacts.json')
            self.end_headers()
            self.wfile.write(json.dumps(contacts, indent=2, ensure_ascii=False).encode('utf-8'))
            print(f"✅ GET /api/contacts/export - Exported {len(contacts)} contacts")
            return
        
        # Serve static files
        file_path = self.path.lstrip('/')
        
        # Root path -> index.html
        if file_path == '' or file_path == '/':
            file_path = 'index.html'
        
        # Check if file exists
        if os.path.exists(file_path) and os.path.isfile(file_path):
            self.send_file(file_path)
            print(f"📄 GET {self.path} - 200 OK")
        else:
            self.send_error(404, 'File not found')
            print(f"❌ GET {self.path} - 404 Not Found")
    
    def do_POST(self):
        """Handle POST requests"""
        
        # API: Create contact
        if self.path == '/api/contacts':
            try:
                # Read body
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
        """Override default log"""
        pass

# ===== MAIN =====
def main():
    # Change to script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    server = HTTPServer(('', PORT), Handler)
    
    print('🚀 Tâm Việt Quang Server')
    print('=' * 50)
    print(f'🌐 Website: http://localhost:{PORT}')
    print(f'📧 API: http://localhost:{PORT}/api/contacts')
    print(f'📊 View contacts: http://localhost:{PORT}/api/contacts')
    print(f'💾 Data: {CONTACTS_FILE}')
    print('=' * 50)
    print('Press Ctrl+C to stop')
    print()
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\n👋 Server stopped')
        server.shutdown()

if __name__ == '__main__':
    main()
