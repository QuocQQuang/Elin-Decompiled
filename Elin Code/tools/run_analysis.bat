@echo off
echo Material Tier Distribution Analyzer
echo ====================================
echo.

echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python from https://python.org
    pause
    exit /b 1
)

echo Python found! Starting analysis...
echo.

echo Option 1: Simple Analysis (no external libraries needed)
echo Option 2: Full Analysis with Charts (requires matplotlib, seaborn, pandas)
echo Option 3: Install dependencies and run full analysis
echo.

set /p choice="Enter choice (1/2/3): "

if "%choice%"=="1" (
    echo Running simple analysis...
    python simple_tier_analyzer.py
) else if "%choice%"=="2" (
    echo Running full analysis...
    python tier_distribution_analyzer.py
) else if "%choice%"=="3" (
    echo Installing dependencies and running full analysis...
    python install_and_run.py
) else (
    echo Invalid choice. Running simple analysis...
    python simple_tier_analyzer.py
)

echo.
echo Analysis completed!
pause
