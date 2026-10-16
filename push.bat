@echo off
setlocal

REM ==========================================
REM Secret Desire - One-click GitHub push
REM ==========================================

cd /d "%~dp0"

set REPO_URL=https://github.com/mathengemuriithi/Secret_desire.git

echo.
echo === Secret Desire deploy ===
echo.

REM Check git is installed
where git >nul 2>nul
if errorlevel 1 (
    echo ERROR: git is not installed or not on PATH.
    echo Download it from https://git-scm.com/download/win
    pause
    exit /b 1
)

REM Initialize repo if needed
if not exist ".git" (
    echo Initializing git repository...
    git init
    git branch -M main
)

REM Set or update remote
git remote get-url origin >nul 2>nul
if errorlevel 1 (
    echo Adding remote origin...
    git remote add origin %REPO_URL%
) else (
    git remote set-url origin %REPO_URL%
)

REM Prompt for commit message
set MSG=%~1
if "%MSG%"=="" (
    set /p MSG="Commit message (press Enter for default): "
)
if "%MSG%"=="" set MSG=Update %DATE% %TIME%

echo.
echo Staging changes...
git add -A

echo.
echo Committing: %MSG%
git commit -m "%MSG%"
if errorlevel 1 (
    echo Nothing to commit, or commit failed.
)

echo.
echo Pushing to %REPO_URL%
git push -u origin main

if errorlevel 1 (
    echo.
    echo Push failed. Common causes:
    echo 1. No credential. Use a Personal Access Token as the password.
    echo    Generate: https://github.com/settings/tokens
    echo 2. Repository does not exist on GitHub. Create it first.
    echo 3. No internet connection.
    pause
    exit /b 1
)

echo.
echo Done. Visit: https://github.com/mathengemuriithi/Secret_desire
echo.
pause
