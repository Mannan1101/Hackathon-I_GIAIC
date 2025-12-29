@echo off
echo Starting Backend Server...
echo.
echo Backend will run on: http://localhost:8000
echo.
cd backend
uvicorn server:app --reload --port 8000
pause
