# Chatbot Setup Guide

## Changes Made:

### 1. Backend Fixes (`backend/main.py`):
   - ✅ Added CORS middleware to allow frontend-backend communication
   - ✅ Changed request parameter from `message` to `question` (matches frontend)
   - ✅ Changed response from `response` to `answer` (matches frontend)

### 2. Frontend Improvements (`frontend/style.css`):
   - ✅ Enhanced chatbot icon with better visibility
   - ✅ Added hover effects for better UX
   - ✅ Increased icon size to 60px x 60px
   - ✅ Added smooth transitions and shadow effects

### 3. Multiple Pages Created:
   - ✅ `index.html` - Home page with chatbot
   - ✅ `about.html` - About page with chatbot
   - ✅ `chapters.html` - Chapters page with chatbot
   - ✅ All pages have navigation links

## How to Run:

### Step 1: Install Backend Dependencies
```bash
cd backend
pip install fastapi uvicorn python-dotenv
```

### Step 2: Start Backend Server
```bash
cd backend
uvicorn main:app --reload --port 8000
```

### Step 3: Open Frontend
Open any of these files in your browser:
- `frontend/index.html`
- `frontend/about.html`
- `frontend/chapters.html`

Or use a local server (recommended):
```bash
cd frontend
python -m http.server 3000
```
Then open: `http://localhost:3000`

## Chatbot Features:

- 💬 **Small chatbot icon** appears on bottom-right of ALL pages
- ✨ **Hover effect** on chatbot icon
- 📱 **Responsive design** - fixed position
- 🔄 **Works on all pages** - index, about, chapters
- 🎨 **Beautiful blue theme** with smooth animations

## Testing:

1. Open any page in browser
2. You should see a blue chatbot icon (💬) at bottom-right
3. Click on the icon to open chat window
4. Type "hello" or "robot" to test the chatbot
5. Navigate between pages - chatbot appears on all pages

## Troubleshooting:

If chatbot icon is not visible:
- Check if backend is running on port 8000
- Open browser console (F12) for any errors
- Make sure `style.css` and `chatbot.js` are loaded
- Clear browser cache and refresh

Enjoy your chatbot! 🚀
