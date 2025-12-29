@echo off
echo Starting Frontend Server...
echo.
echo Open your browser and go to: http://localhost:8080
echo.
cd frontend
python -m http.server 8080
pause
