@echo off
rem Card-review console launcher.
rem Double-click me: starts the local server, then opens the console in the browser.
cd /d "%~dp0"
start "Review Server - close me to stop" cmd /k node review_server.js
timeout /t 2 /nobreak >nul
start "" http://127.0.0.1:8765/review_console.html
