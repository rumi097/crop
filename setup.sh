#!/bin/bash

# Setup script for Crop Recommendation System
# Run this script to set up the entire project

set -e  # Exit on error

echo "======================================================================"
echo "Crop Recommendation System - Setup Script"
echo "======================================================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check Python installation
echo "Checking Python installation..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo -e "${GREEN}✓${NC} Python found: $PYTHON_VERSION"
else
    echo -e "${RED}✗${NC} Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check Node.js installation
echo "Checking Node.js installation..."
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    echo -e "${GREEN}✓${NC} Node.js found: $NODE_VERSION"
else
    echo -e "${RED}✗${NC} Node.js is not installed. Please install Node.js 14 or higher."
    exit 1
fi

echo ""
echo "======================================================================"
echo "Setting up Backend..."
echo "======================================================================"
echo ""

# Create backend virtual environment
cd backend
echo "Creating Python virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install Python dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo -e "${GREEN}✓${NC} Backend dependencies installed"

# Create necessary directories
echo "Creating necessary directories..."
mkdir -p saved_models
mkdir -p uploads
touch uploads/.gitkeep

cd ..

# Generate sample dataset
echo ""
echo "======================================================================"
echo "Generating Sample Dataset..."
echo "======================================================================"
echo ""

cd data
mkdir -p fertilizer_images/train/{Healthy,Contaminated,Expired,Fake,Damaged}
mkdir -p fertilizer_images/val/{Healthy,Contaminated,Expired,Fake,Damaged}

if [ ! -f "crop_recommendation.csv" ]; then
    echo "Generating sample crop recommendation dataset..."
    source ../backend/venv/bin/activate
    python generate_sample_data.py
    echo -e "${GREEN}✓${NC} Sample dataset generated"
else
    echo -e "${YELLOW}ℹ${NC} Dataset already exists, skipping generation"
fi

cd ..

# Train models
echo ""
echo "======================================================================"
echo "Training Models..."
echo "======================================================================"
echo ""

read -p "Do you want to train the models now? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    cd scripts
    source ../backend/venv/bin/activate
    
    echo "Training crop recommendation model..."
    python train_crop_model.py
    
    echo ""
    echo -e "${YELLOW}Note:${NC} CNN model training requires image dataset."
    echo "Please add images to data/fertilizer_images/ directory and run:"
    echo "  python scripts/train_cnn_model.py"
    
    cd ..
else
    echo -e "${YELLOW}ℹ${NC} Skipping model training. You can train later using:"
    echo "  cd scripts && python train_crop_model.py"
fi

# Setup frontend
echo ""
echo "======================================================================"
echo "Setting up Frontend..."
echo "======================================================================"
echo ""

cd frontend

echo "Installing Node.js dependencies..."
npm install

echo -e "${GREEN}✓${NC} Frontend dependencies installed"

cd ..

# Create .env file
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cp .env.example .env
    echo -e "${GREEN}✓${NC} .env file created"
fi

# Final instructions
echo ""
echo "======================================================================"
echo "✓ Setup Complete!"
echo "======================================================================"
echo ""
echo "To start the application:"
echo ""
echo "1. Start Backend (Terminal 1):"
echo "   ${GREEN}cd backend${NC}"
echo "   ${GREEN}source venv/bin/activate${NC}"
echo "   ${GREEN}python app.py${NC}"
echo ""
echo "2. Start Frontend (Terminal 2):"
echo "   ${GREEN}cd frontend${NC}"
echo "   ${GREEN}npm start${NC}"
echo ""
echo "3. Open browser:"
echo "   ${GREEN}http://localhost:3000${NC}"
echo ""
echo "======================================================================"
echo "📚 Documentation:"
echo "   - README.md - Full documentation"
echo "   - QUICKSTART.md - Quick start guide"
echo "======================================================================"
echo ""
echo "For dataset download:"
echo "  Crop Data: https://www.kaggle.com/atharvaingle/crop-recommendation-dataset"
echo ""
echo -e "${GREEN}Happy Farming! 🌱${NC}"
