@echo off
echo ========================================
echo   Starting Complete Book Chatbot System
echo ========================================
echo.
echo This will start:
echo   1. Backend Server (Port 8000)
echo   2. Docusaurus Website (Port 3000)
echo.
echo Press any key to continue...
pause >nul
echo.

echo Starting Backend Server...
start "Backend Server" cmd /k "cd backend && uvicorn main:app --reload --port 8000"

timeout /t 3 >nul

echo Starting Docusaurus Website...
start "Docusaurus Site" cmd /k "npm start"

echo.
echo ========================================
echo   All Services Started!
echo ========================================
echo.
echo Backend:  http://localhost:8000
echo Website:  http://localhost:3000
echo.
echo Chatbot icon will appear on bottom-right of all pages!
echo.
echo Close this window to keep servers running.
echo Close individual windows to stop specific services.
echo.
pause
