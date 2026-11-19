@echo off
title Jinghui One-Click Launcher
setlocal
cd /d "%~dp0"

echo ================================================
echo   Jinghui (JingHui) One-Click Launcher
echo   Frontend: http://localhost:5173
echo   Backend : http://127.0.0.1:8000
echo ================================================
echo.

REM ---------- 1. Check backend environment ----------
if not exist "server\.venv\Scripts\uvicorn.exe" (
    echo [Setup] Backend venv not found. Creating it now...
    pushd server
    python -m venv .venv
    .venv\Scripts\python.exe -m pip install -r requirements.txt
    if errorlevel 1 (
        echo [Error] Backend dependency installation failed. Check Python and network.
        popd
        pause
        exit /b 1
    )
    popd
    echo [Setup] Backend environment ready.
)

REM ---------- 2. Check frontend dependencies ----------
if not exist "web\node_modules" (
    echo [Setup] Frontend node_modules not found. Installing now...
    pushd web
    call npm install
    if errorlevel 1 (
        echo [Error] Frontend dependency installation failed. Check Node.js and network.
        popd
        pause
        exit /b 1
    )
    popd
    echo [Setup] Frontend dependencies ready.
)

REM ---------- 3. Start backend (port 8000) if not already running ----------
netstat -ano | findstr "LISTENING" | findstr ":8000 " >nul 2>&1
if %errorlevel%==0 (
    echo [Skip] Backend is already running on port 8000.
) else (
    echo [Start] Launching backend on port 8000 ...
    start "Jinghui Backend 8000" cmd /k "cd /d %~dp0server && .venv\Scripts\uvicorn.exe app.main:app --host 127.0.0.1 --port 8000"
)

REM ---------- 4. Start frontend (port 5173) if not already running ----------
netstat -ano | findstr "LISTENING" | findstr ":5173 " >nul 2>&1
if %errorlevel%==0 (
    echo [Skip] Frontend is already running on port 5173.
) else (
    echo [Start] Launching frontend on port 5173 ...
    start "Jinghui Frontend 5173" cmd /k "cd /d %~dp0web && npm run dev"
)

REM ---------- 5. Wait for services and open browser ----------
echo [Wait] Giving services a few seconds to boot ...
ping -n 9 127.0.0.1 >nul
start "" http://localhost:5173

echo.
echo [Done] Browser should now open at http://localhost:5173
echo        Demo user : demo@jinghui.art / Demo123456
echo        Admin     : admin@jinghui.art / Admin123456
echo.
echo To stop the site: close the two Jinghui windows,
echo or press Ctrl+C inside each window.
echo.
ping -n 7 127.0.0.1 >nul
endlocal
exit /b 0
