@echo off
setlocal

REM ==========================================
REM Secret Desire - One-click Django server
REM ==========================================

cd /d "%~dp0"

set PORT=8000
set HOST=127.0.0.1

echo.
echo === Secret Desire server ===
echo.

REM Check Python is installed
where python >nul 2>nul
if errorlevel 1 (
    echo ERROR: python is not installed or not on PATH.
    echo Download it from https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Check manage.py exists
if not exist "manage.py" (
    echo ERROR: manage.py not found in this folder.
    echo Place start_server.bat next to manage.py.
    echo Current folder: %CD%
    pause
    exit /b 1
)

REM Auto-detect virtual environment
set VENV=
if exist "venv\Scripts\activate.bat"   set VENV=venv
if exist ".venv\Scripts\activate.bat"  set VENV=.venv
if exist "env\Scripts\activate.bat"    set VENV=env

if "%VENV%"=="" (
    echo ERROR: No virtual environment found.
    echo Expected one of: venv\ , .venv\ , env\
    echo Create one with: python -m venv venv
    pause
    exit /b 1
)

echo Activating %VENV% ...
call "%VENV%\Scripts\activate.bat"
if errorlevel 1 (
    echo ERROR: Failed to activate %VENV%.
    pause
    exit /b 1
)

REM Quick dependency sanity check
python -c "import django" >nul 2>nul
if errorlevel 1 (
    echo ERROR: Django is not installed in this environment.
    echo Run: pip install -r requirements.txt
    pause
    exit /b 1
)

REM Apply migrations (safe if nothing pending)
echo.
echo Applying migrations...
python manage.py migrate --noinput
if errorlevel 1 (
    echo WARNING: migrate reported an error. Continuing anyway.
)

REM Collect static files (only if STATIC_ROOT is configured; safe otherwise)
echo.
echo Collecting static files...
python manage.py collectstatic --noinput >nul 2>nul

echo.
echo Server starting at http://%HOST%:%PORT%
echo Press CTRL+C to stop.
echo.

REM Open browser after ~2s (non-blocking)
start "" cmd /c "timeout /t 2 >nul & start http://%HOST%:%PORT%"

REM Start the Django dev server
python manage.py runserver %HOST%:%PORT%

echo.
echo === Server stopped ===
if errorlevel 1 (
    echo.
    echo Server exited with an error. Common causes:
    echo 1. Port %PORT% already in use - change PORT at the top.
    echo 2. Missing dependency - run: pip install -r requirements.txt
    echo 3. Unapplied model changes - run: python manage.py makemigrations
    echo 4. Missing .env / SECRET_KEY / database config.
    echo 5. Settings module path wrong - check DJANGO_SETTINGS_MODULE.
)
echo.
pause
endlocal
