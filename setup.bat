@echo off
REM Setup script for Crop Recommendation System (Windows)
REM Run this script to set up the entire project

echo ======================================================================
echo Crop Recommendation System - Setup Script (Windows)
echo ======================================================================
echo.

REM Check Python installation
echo Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [X] Python is not installed. Please install Python 3.8 or higher.
    exit /b 1
)
echo [OK] Python found

REM Check Node.js installation
echo Checking Node.js installation...
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [X] Node.js is not installed. Please install Node.js 14 or higher.
    exit /b 1
)
echo [OK] Node.js found

echo.
echo ======================================================================
echo Setting up Backend...
echo ======================================================================
echo.

REM Create backend virtual environment
cd backend
echo Creating Python virtual environment...
python -m venv venv

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install Python dependencies
echo Installing Python dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt

echo [OK] Backend dependencies installed

REM Create necessary directories
echo Creating necessary directories...
if not exist "saved_models" mkdir saved_models
if not exist "uploads" mkdir uploads

cd ..

REM Generate sample dataset
echo.
echo ======================================================================
echo Generating Sample Dataset...
echo ======================================================================
echo.

cd data
if not exist "fertilizer_images\train" mkdir fertilizer_images\train
if not exist "fertilizer_images\val" mkdir fertilizer_images\val

if not exist "crop_recommendation.csv" (
    echo Generating sample crop recommendation dataset...
    call ..\backend\venv\Scripts\activate.bat
    python generate_sample_data.py
    echo [OK] Sample dataset generated
) else (
    echo [i] Dataset already exists, skipping generation
)

cd ..

REM Train models
echo.
echo ======================================================================
echo Training Models...
echo ======================================================================
echo.

set /p TRAIN="Do you want to train the models now? (y/n): "
if /i "%TRAIN%"=="y" (
    cd scripts
    call ..\backend\venv\Scripts\activate.bat
    
    echo Training crop recommendation model...
    python train_crop_model.py
    
    echo.
    echo [Note] CNN model training requires image dataset.
    echo Please add images to data\fertilizer_images\ directory and run:
    echo   python scripts\train_cnn_model.py
    
    cd ..
) else (
    echo [i] Skipping model training. You can train later using:
    echo   cd scripts ^&^& python train_crop_model.py
)

REM Setup frontend
echo.
echo ======================================================================
echo Setting up Frontend...
echo ======================================================================
echo.

cd frontend

echo Installing Node.js dependencies...
call npm install

echo [OK] Frontend dependencies installed

cd ..

REM Create .env file
if not exist ".env" (
    echo Creating .env file...
    copy .env.example .env
    echo [OK] .env file created
)

REM Final instructions
echo.
echo ======================================================================
echo [OK] Setup Complete!
echo ======================================================================
echo.
echo To start the application:
echo.
echo 1. Start Backend (Terminal 1):
echo    cd backend
echo    venv\Scripts\activate
echo    python app.py
echo.
echo 2. Start Frontend (Terminal 2):
echo    cd frontend
echo    npm start
echo.
echo 3. Open browser:
echo    http://localhost:3000
echo.
echo ======================================================================
echo Documentation:
echo    - README.md - Full documentation
echo    - QUICKSTART.md - Quick start guide
echo ======================================================================
echo.
echo For dataset download:
echo   Crop Data: https://www.kaggle.com/atharvaingle/crop-recommendation-dataset
echo.
echo Happy Farming!
pause
