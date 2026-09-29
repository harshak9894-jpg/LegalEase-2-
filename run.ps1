# LegalEase Startup Script for Windows PowerShell
Write-Host "========================================" -ForegroundColor Cyan
Write-Host " Starting LegalEase (Backend + Frontend)" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

$pyBin = "python"
if (Test-Path "venv\Scripts\python.exe") {
    $pyBin = "venv\Scripts\python.exe"
} elseif (Test-Path ".venv\Scripts\python.exe") {
    $pyBin = ".venv\Scripts\python.exe"
}

$stBin = "streamlit"
if (Test-Path "venv\Scripts\streamlit.exe") {
    $stBin = "venv\Scripts\streamlit.exe"
} elseif (Test-Path ".venv\Scripts\streamlit.exe") {
    $stBin = ".venv\Scripts\streamlit.exe"
}

# Start Backend Server
Write-Host "Starting FastAPI Backend on port 8001..." -ForegroundColor Yellow
$backend = Start-Process -PassThru powershell -ArgumentList "-Command", "$pyBin -m uvicorn legalEaseAPI.main:app --host 127.0.0.1 --port 8001 --reload"

Start-Sleep -Seconds 2

# Start Streamlit Frontend
Write-Host "Starting Streamlit Frontend on port 8501..." -ForegroundColor Green
& $stBin run frontend/app.py --server.port 8501
