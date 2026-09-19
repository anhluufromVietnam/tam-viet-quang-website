#!/usr/bin/env python3
"""
Tâm Việt Quang - Contact API Server
Chạy trên port 3961
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import os
from datetime import datetime
from urllib.parse import parse_qs
import re

# File lưu contacts
DATA_DIR = 'data'
CONTACTS_FILE = os.path.join(DATA_DIR, 'contacts.json')

# Tạo thư mục data nếu chưa có
os.makedirs(DATA_DIR, exist_ok=True)

# Khởi tạo file contacts nếu chưa có
if not os.path.exists(CONTACTS_FILE):
    with open(CONTACTS_FILE, 'w', encoding='utf-8') as f:
        json.dump([], f)

def load_contacts():
    """Đọc contacts từ file"""
    try:
        with open(CONTACTS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []

def save_contacts(contacts):
    """Lưu contacts vào file"""
    with open(CONTACTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(contacts, f, indent=2, ensure_ascii=False)

def validate_email(email):
    """Validate email format"""
    pattern = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
    return re.match(pattern, email) is not None

class ContactAPIHandler(BaseHTTPRequestHandler):
    """Handler cho Contact API"""
    
    def send_cors_headers(self):
        """Gửi CORS headers"""
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
    
    def send_json_response(self, status_code, data):
        """Gửi JSON response"""
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_cors_headers()
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))
    
    def do_OPTIONS(self):
        """Handle OPTIONS request (CORS preflight)"""
        self.send_response(200)
        self.send_cors_headers()
        self.end_headers()
    
    def do_GET(self):
        """Handle GET requests"""
        
        # GET /api/contacts - Lấy tất cả contacts
        if self.path == '/api/contacts':
            contacts = load_contacts()
            self.send_json_response(200, {
                'success': True,
                'count': len(contacts),
                'data': contacts
            })
            print(f"✅ GET /api/contacts - {len(contacts)} contacts")
        
        # GET /api/contacts/export - Export contacts
        elif self.path == '/api/contacts/export':
            contacts = load_contacts()
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Content-Disposition', 'attachment; filename=contacts.json')
            self.send_cors_headers()
            self.end_headers()
            self.wfile.write(json.dumps(contacts, indent=2, ensure_ascii=False).encode('utf-8'))
            print(f"✅ GET /api/contacts/export - Exported {len(contacts)} contacts")
        
        else:
            self.send_json_response(404, {
                'success': False,
                'message': 'Endpoint not found'
            })
    
    def do_POST(self):
        """Handle POST requests"""
        
        # POST /api/contacts - Tạo contact mới
        if self.path == '/api/contacts':
            try:
                # Đọc body
                content_length = int(self.headers.get('Content-Length', 0))
                body = self.rfile.read(content_length).decode('utf-8')
                data = json.loads(body)
                
                # Validate
                name = data.get('name', '').strip()
                email = data.get('email', '').strip()
                company = data.get('company', '').strip()
                message = data.get('message', '').strip()
                
                if not name or not email or not message:
                    self.send_json_response(400, {
                        'success': False,
                        'message': 'Vui lòng điền đầy đủ thông tin bắt buộc (Họ tên, Email, Tin nhắn)'
                    })
                    return
                
                if not validate_email(email):
                    self.send_json_response(400, {
                        'success': False,
                        'message': 'Email không hợp lệ'
                    })
                    return
                
                # Tạo contact mới
                new_contact = {
                    'id': str(int(datetime.now().timestamp() * 1000)),
                    'name': name,
                    'email': email,
                    'company': company,
                    'message': message,
                    'timestamp': datetime.now().isoformat(),
                    'status': 'new'
                }
                
                # Lưu
                contacts = load_contacts()
                contacts.append(new_contact)
                save_contacts(contacts)
                
                print(f"✅ POST /api/contacts - New contact saved: {name} <{email}>")
                
                self.send_json_response(201, {
                    'success': True,
                    'message': 'Gửi thành công! Chúng tôi sẽ liên hệ với bạn sớm nhất.',
                    'data': new_contact
                })
                
            except Exception as e:
                print(f"❌ Error: {e}")
                self.send_json_response(500, {
                    'success': False,
                    'message': 'Có lỗi xảy ra. Vui lòng thử lại sau.',
                    'error': str(e)
                })
        
        else:
            self.send_json_response(404, {
                'success': False,
                'message': 'Endpoint not found'
            })
    
    def do_PATCH(self):
        """Handle PATCH requests"""
        
        # PATCH /api/contacts/:id - Cập nhật status
        if self.path.startswith('/api/contacts/'):
            try:
                contact_id = self.path.split('/')[-1]
                
                # Đọc body
                content_length = int(self.headers.get('Content-Length', 0))
                body = self.rfile.read(content_length).decode('utf-8')
                data = json.loads(body)
                
                contacts = load_contacts()
                found = False
                
                for contact in contacts:
                    if contact['id'] == contact_id:
                        contact['status'] = data.get('status', contact['status'])
                        contact['updatedAt'] = datetime.now().isoformat()
                        found = True
                        break
                
                if not found:
                    self.send_json_response(404, {
                        'success': False,
                        'message': 'Contact not found'
                    })
                    return
                
                save_contacts(contacts)
                
                print(f"✅ PATCH /api/contacts/{contact_id} - Updated")
                
                self.send_json_response(200, {
                    'success': True,
                    'message': 'Contact updated'
                })
                
            except Exception as e:
                self.send_json_response(500, {
                    'success': False,
                    'message': 'Error updating contact',
                    'error': str(e)
                })
    
    def do_DELETE(self):
        """Handle DELETE requests"""
        
        # DELETE /api/contacts/:id - Xóa contact
        if self.path.startswith('/api/contacts/'):
            try:
                contact_id = self.path.split('/')[-1]
                
                contacts = load_contacts()
                filtered = [c for c in contacts if c['id'] != contact_id]
                
                if len(filtered) == len(contacts):
                    self.send_json_response(404, {
                        'success': False,
                        'message': 'Contact not found'
                    })
                    return
                
                save_contacts(filtered)
                
                print(f"✅ DELETE /api/contacts/{contact_id} - Deleted")
                
                self.send_json_response(200, {
                    'success': True,
                    'message': 'Contact deleted'
                })
                
            except Exception as e:
                self.send_json_response(500, {
                    'success': False,
                    'message': 'Error deleting contact',
                    'error': str(e)
                })
    
    def log_message(self, format, *args):
        """Override log message"""
        pass  # Tắt log mặc định

def main():
    """Chạy server"""
    port = 3961
    
    server = HTTPServer(('', port), ContactAPIHandler)
    
    print('🚀 Tâm Việt Quang Contact API Server Started')
    print(f'📍 Server running at: http://localhost:{port}')
    print(f'📧 Contact API: http://localhost:{port}/api/contacts')
    print(f'📊 View contacts: http://localhost:{port}/api/contacts')
    print(f'💾 Data file: {CONTACTS_FILE}')
    print('Press Ctrl+C to stop the server')
    print()
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\n\n👋 Server stopped')
        server.shutdown()

if __name__ == '__main__':
    main()
