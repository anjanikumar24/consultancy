@echo off
REM One-time setup for Windows. Run from this folder:  setup_windows.bat
python -m venv env || goto :error
call env\Scripts\activate.bat || goto :error
python -m pip install --upgrade pip
pip install -r requirements.txt || goto :error
if not exist .env copy .env.example .env
python manage.py makemigrations core || goto :error
python manage.py migrate || goto :error
echo.
echo Create your admin login now:
python manage.py createsuperuser
echo.
echo Done. Start the site with:   env\Scripts\activate  then  python manage.py runserver
echo Website: http://127.0.0.1:8000/   Admin panel: http://127.0.0.1:8000/admin/
goto :eof
:error
echo Setup failed. Read the message above.
exit /b 1
