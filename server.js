const express = require('express');
const cors = require('cors');
const fs = require('fs');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.static(__dirname));

// Data file path
const CONTACTS_FILE = path.join(__dirname, 'data', 'contacts.json');

// Ensure data directory exists
const dataDir = path.join(__dirname, 'data');
if (!fs.existsSync(dataDir)) {
    fs.mkdirSync(dataDir, { recursive: true });
}

// Initialize contacts file if it doesn't exist
if (!fs.existsSync(CONTACTS_FILE)) {
    fs.writeFileSync(CONTACTS_FILE, JSON.stringify([], null, 2));
}

// API Routes

// Get all contacts
app.get('/api/contacts', (req, res) => {
    try {
        const contacts = JSON.parse(fs.readFileSync(CONTACTS_FILE, 'utf8'));
        res.json({
            success: true,
            count: contacts.length,
            data: contacts
        });
    } catch (error) {
        res.status(500).json({
            success: false,
            message: 'Error reading contacts',
            error: error.message
        });
    }
});

// Submit new contact
app.post('/api/contacts', (req, res) => {
    try {
        const { name, email, company, message } = req.body;
        
        // Validation
        if (!name || !email || !message) {
            return res.status(400).json({
                success: false,
                message: 'Vui lòng điền đầy đủ thông tin bắt buộc (Họ tên, Email, Tin nhắn)'
            });
        }

        // Email validation
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(email)) {
            return res.status(400).json({
                success: false,
                message: 'Email không hợp lệ'
            });
        }

        // Read existing contacts
        const contacts = JSON.parse(fs.readFileSync(CONTACTS_FILE, 'utf8'));

        // Create new contact
        const newContact = {
            id: Date.now().toString(),
            name,
            email,
            company: company || '',
            message,
            timestamp: new Date().toISOString(),
            status: 'new' // new, read, replied
        };

        // Add to contacts
        contacts.push(newContact);

        // Save to file
        fs.writeFileSync(CONTACTS_FILE, JSON.stringify(contacts, null, 2));

        console.log('✅ New contact saved:', newContact);

        res.status(201).json({
            success: true,
            message: 'Gửi thành công! Chúng tôi sẽ liên hệ với bạn sớm nhất.',
            data: newContact
        });

    } catch (error) {
        console.error('❌ Error saving contact:', error);
        res.status(500).json({
            success: false,
            message: 'Có lỗi xảy ra. Vui lòng thử lại sau.',
            error: error.message
        });
    }
});

// Update contact status
app.patch('/api/contacts/:id', (req, res) => {
    try {
        const { id } = req.params;
        const { status } = req.body;

        const contacts = JSON.parse(fs.readFileSync(CONTACTS_FILE, 'utf8'));
        const index = contacts.findIndex(c => c.id === id);

        if (index === -1) {
            return res.status(404).json({
                success: false,
                message: 'Contact not found'
            });
        }

        contacts[index].status = status;
        contacts[index].updatedAt = new Date().toISOString();

        fs.writeFileSync(CONTACTS_FILE, JSON.stringify(contacts, null, 2));

        res.json({
            success: true,
            message: 'Contact updated',
            data: contacts[index]
        });

    } catch (error) {
        res.status(500).json({
            success: false,
            message: 'Error updating contact',
            error: error.message
        });
    }
});

// Delete contact
app.delete('/api/contacts/:id', (req, res) => {
    try {
        const { id } = req.params;
        const contacts = JSON.parse(fs.readFileSync(CONTACTS_FILE, 'utf8'));
        const filtered = contacts.filter(c => c.id !== id);

        if (filtered.length === contacts.length) {
            return res.status(404).json({
                success: false,
                message: 'Contact not found'
            });
        }

        fs.writeFileSync(CONTACTS_FILE, JSON.stringify(filtered, null, 2));

        res.json({
            success: true,
            message: 'Contact deleted'
        });

    } catch (error) {
        res.status(500).json({
            success: false,
            message: 'Error deleting contact',
            error: error.message
        });
    }
});

// Export contacts as JSON
app.get('/api/contacts/export', (req, res) => {
    try {
        const contacts = JSON.parse(fs.readFileSync(CONTACTS_FILE, 'utf8'));
        res.setHeader('Content-Type', 'application/json');
        res.setHeader('Content-Disposition', 'attachment; filename=contacts.json');
        res.send(JSON.stringify(contacts, null, 2));
    } catch (error) {
        res.status(500).json({
            success: false,
            message: 'Error exporting contacts',
            error: error.message
        });
    }
});

// Serve index.html for root
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'index.html'));
});

// Start server
app.listen(PORT, () => {
    console.log('🚀 Tâm Việt Quang Server Started');
    console.log(`📍 Server running at: http://localhost:${PORT}`);
    console.log(`📧 Contact API: http://localhost:${PORT}/api/contacts`);
    console.log(`📊 View contacts: http://localhost:${PORT}/api/contacts`);
    console.log('Press Ctrl+C to stop the server');
});
