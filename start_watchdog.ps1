Set-Location $PSScriptRoot

function Start-Watchdog {
    Clear-Host
    Write-Host "========================================================" -ForegroundColor Cyan
    Write-Host "       YUKI WATCHDOG - PERSISTENT MODE" -ForegroundColor White
    Write-Host "========================================================" -ForegroundColor Cyan
    Write-Host ""

    if (Test-Path "venv\Scripts\Activate.ps1") {
        . venv\Scripts\Activate.ps1
    }
    else {
        Write-Host "Virtual environment not found, trying with global python..." -ForegroundColor Yellow
    }

    Write-Host "Starting Yuki Watchdog (Process Monitor)..." -ForegroundColor Green
    Write-Host "[Press Ctrl+C to stop the monitoring loop]" -ForegroundColor Gray
    Write-Host ""

    # Start the process and wait for it to finish
    python yuki_watchdog.py

    Write-Host ""
    Write-Host "========================================================" -ForegroundColor Red
    Write-Host "Watchdog process ended. Restarting in 5 seconds..." -ForegroundColor Red
    Write-Host "========================================================" -ForegroundColor Red
    Start-Sleep -Seconds 5
}

while ($true) {
    Start-Watchdog
}
