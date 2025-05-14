@echo off
cd /d D:\Joseph\king\E_commerce
call venv\Scripts\activate
cd src
daphne -b 0.0.0.0 -p 8000 E_commerce.asgi:application
pause
