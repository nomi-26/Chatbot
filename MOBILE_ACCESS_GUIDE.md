# Mobile Access Guide for Gemini AI Chat

## Problem Fixed
The JavaScript file had a hardcoded API URL: `http://localhost:5000/api/chat`
This prevented mobile devices from connecting because "localhost" refers to the mobile device itself, not your computer.

## Solution Applied
Changed the API URL to use relative path: `/api/chat`
This allows the browser to automatically use the current host (your computer's IP when accessed remotely).

## How to Test Mobile Access

### Step 1: Start Flask Server
```bash
cd "web codes/gen-ai project"
python app.py
```

### Step 2: Find Your Computer's IP Address
- Windows: Open Command Prompt and type `ipconfig`
- Look for "IPv4 Address" (usually starts with 192.168.x.x)

### Step 3: Port Forwarding Setup
1. Make sure your computer and mobile are on the same WiFi network
2. Configure your router to forward port 5000 to your computer's IP
3. Or use a service like ngrok for temporary access

### Step 4: Access from Mobile
Open mobile browser and go to: `http://YOUR_COMPUTER_IP:5000`

### Step 5: Test Chat Functionality
- Type a message in the chat
- It should now work from your mobile device

## Troubleshooting

### If it still doesn't work:
1. Check firewall settings on your computer
2. Verify Flask is running on 0.0.0.0 (not just localhost)
3. Ensure mobile and computer are on same network
4. Try accessing from another device on the same network first

### Flask Server Command (for external access):
```bash
python app.py --host=0.0.0.0 --port=5000
```

## Security Note
- The API key is hardcoded in the app.py file
- Consider using environment variables for production
- Only use port forwarding on trusted networks
