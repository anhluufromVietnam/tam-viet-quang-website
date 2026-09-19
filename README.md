# Tâm Việt Quang Website

Website chính thức của **Công ty Cổ phần Phát triển Thương mại Công nghệ Tâm Việt Quang**

## 🚀 Cài đặt và chạy

### 1. Cài đặt dependencies
```bash
npm install
```

### 2. Chạy server
```bash
npm start
```

### 3. Truy cập website
Mở trình duyệt và truy cập: **http://localhost:3000**

## 📧 API Endpoints

### Submit Contact Form
```
POST /api/contacts
```

Body:
```json
{
  "name": "Nguyễn Văn A",
  "email": "email@example.com",
  "company": "Công ty ABC",
  "message": "Nội dung tin nhắn"
}
```

### Get All Contacts
```
GET /api/contacts
```

Response:
```json
{
  "success": true,
  "count": 10,
  "data": [...]
}
```

### Export Contacts
```
GET /api/contacts/export
```
Tải file JSON chứa tất cả contacts.

### Update Contact Status
```
PATCH /api/contacts/:id
```

Body:
```json
{
  "status": "read"
}
```

### Delete Contact
```
DELETE /api/contacts/:id
```

## 📁 Cấu trúc dữ liệu

Contacts được lưu trong file `data/contacts.json`:

```json
[
  {
    "id": "1234567890",
    "name": "Nguyễn Văn A",
    "email": "email@example.com",
    "company": "Công ty ABC",
    "message": "Nội dung tin nhắn",
    "timestamp": "2026-09-19T00:15:00.000Z",
    "status": "new"
  }
]
```

## 🎨 Brand Colors

| Màu | Vai trò | Mã màu |
|-----|---------|--------|
| 🔵 Xanh tím / Royal Blue | Màu chủ đạo | `#4B4ACB` |
| 🟢 Xanh lá / Emerald Green | Màu phụ | `#4CAF75` |
| ⚫ Đen | Chữ & text | `#111111` |
| ⚪ Trắng | Nền | `#FFFFFF` |

## 📁 Cấu trúc thư mục

```
tam-viet-quang-website/
├── index.html              # Trang chủ
├── css/
│   └── styles.css          # Stylesheet chính
├── js/
│   └── main.js             # JavaScript
├── images/
│   ├── logo/               # Logo công ty
│   │   └── logo.png        # (placeholder)
│   ├── banner/             # Hình ảnh banner
│   │   ├── hero-illustration.png
│   │   └── about-image.png
│   ├── products/           # Hình ảnh sản phẩm
│   │   ├── vyiq-platform.png
│   │   ├── ai-chatbot.png
│   │   ├── robot.png
│   │   └── iot-solution.png
│   ├── team/               # Hình ảnh đội ngũ
│   ├── icons/              # Icons
│   │   ├── tech-icon.png
│   │   ├── ai-icon.png
│   │   ├── robotics-icon.png
│   │   ├── education-icon.png
│   │   ├── media-icon.png
│   │   └── travel-icon.png
│   └── README.md           # Hướng dẫn ảnh
└── README.md               # File này
```

## 🏢 Thông tin công ty

- **Tên đầy đủ:** Công ty Cổ phần Phát triển Thương mại Công nghệ Tâm Việt Quang
- **Tên tiếng Anh:** TAM VIET QUANG TECHNOLOGY TRADING DEVELOPMENT JOINT STOCK COMPANY
- **Email:** techvietquang@edu-verse.id.vn
- **Điện thoại:** +84 928 265 183
- **Mã số thuế:** 0111027462
- **Địa chỉ:** 69 Ái Mộ, Hà Nội, Việt Nam
- **Ngày thành lập:** 17/04/2025

## 🚀 Lĩnh vực hoạt động

### 💻 Technology & Software
- Lập trình máy tính & phần mềm
- Tư vấn CNTT & quản trị hệ thống
- Dịch vụ công nghệ thông tin
- Xử lý dữ liệu & Big Data

### 🧠 VyIQ - AI Platform
- Modular AI Platform
- Conversational Intelligence
- AI Agent & Automation
- Software Integration
- Robotic Integration

### 🦾 Robotics & Hardware
- Robot tích hợp AI
- Thiết bị nhúng & Embedded
- AIoT & Smart Devices

### 🎓 Education & EdTech
- AI Virtual Assistant cho giáo dục
- Giáo dục AI & Robotics
- E-learning Platform

### 🎬 Media & Events
- Quảng cáo & Digital Marketing
- Tổ chức sự kiện
- Sản xuất phim & video

### ✈️ Travel & Tourism
- Đại lý du lịch
- Điều hành tour
- Travel Tech Solutions

## 🖼️ Hướng dẫn sử dụng ảnh

### Kích thước khuyến nghị

| Loại ảnh | Kích thước | Định dạng |
|----------|------------|-----------|
| Logo | 512x512px | PNG (transparent) |
| Hero Banner | 1920x1080px | PNG/JPG |
| Product Image | 800x600px | PNG/JPG |
| Icon | 128x128px | PNG (transparent) |
| Team Photo | 400x400px | JPG |

### Placeholder Images

Hiện tại tất cả các vị trí ảnh đều có placeholder. Để thay thế:

1. Thêm ảnh vào thư mục tương ứng trong `images/`
2. Đảm bảo tên file khớp với đường dẫn trong HTML
3. Tối ưu kích thước ảnh trước khi upload

## 🌐 Deployment

### Local Development
```bash
# Mở trực tiếp file index.html trong trình duyệt
# Hoặc sử dụng live server
npx serve .
```

### GitHub Pages
1. Push code lên GitHub repository
2. Vào Settings > Pages
3. Chọn branch và folder root
4. Website sẽ có tại: `https://[username].github.io/[repo-name]`

## 📱 Responsive Design

Website hỗ trợ đầy đủ các kích thước màn hình:
- Desktop: > 1024px
- Tablet: 768px - 1024px
- Mobile: < 768px

## 📄 License

© 2025 Công ty Cổ phần Phát triển Thương mại Công nghệ Tâm Việt Quang. All rights reserved.

---

**From AI to the Physical World** 🚀
