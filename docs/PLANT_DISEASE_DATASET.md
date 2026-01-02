# Plant Disease Detection Model - CCMT Dataset

This document provides instructions for training the plant disease detection model using the CCMT Multi-Crop Plant Disease Detection Dataset.

## 📦 Dataset Information

- **Name**: CCMT Multi-Crop Plant Disease Detection Dataset
- **Source**: [Kaggle Dataset](https://www.kaggle.com/datasets/shawontmsez/ccmt-multi-crop-plant-disease-detection-dataset)
- **Size**: ~8 GB
- **Total Images**: 130,378
  - Raw Data: 25,126 images
  - Augmented Data: 105,252 images
- **Image Format**: JPEG (400×400 pixels, RGB)
- **Crops**: 4 (Cashew, Cassava, Maize, Tomato)
- **Disease Classes**: 22 total

### Disease Classes by Crop

#### Cashew (5 classes)
- Anthracnose
- Gumosis
- Healthy
- Leaf Miner
- Red Rust

#### Cassava (5 classes)
- Bacterial Blight
- Brown Spot
- Green Mite
- Healthy
- Mosaic

#### Maize (7 classes)
- Fall Armyworm
- Grasshopper
- Healthy
- Leaf Beetle
- Leaf Blight
- Leaf Spot
- Streak Virus

#### Tomato (5 classes)
- Healthy
- Leaf Blight
- Leaf Curl
- Septoria Leaf Spot
- Verticillium Wilt

## 📥 Download Instructions

### Method 1: Manual Download (Recommended)

1. **Visit Kaggle Dataset Page**
   ```
   https://www.kaggle.com/datasets/shawontmsez/ccmt-multi-crop-plant-disease-detection-dataset
   ```

2. **Sign in to Kaggle** (create free account if needed)

3. **Click Download Button** (top right of dataset page)

4. **Extract the ZIP file**
   - File will be named: `ccmt-multi-crop-plant-disease-detection-dataset.zip`
   - Extract contents to get the `data` folder

5. **Move to Project Directory**
   ```bash
   # Create the target directory
   mkdir -p data/plant_diseases
   
   # Move the extracted folders
   mv path/to/extracted/data/* data/plant_diseases/
   ```

6. **Verify Structure**
   Your folder structure should look like:
   ```
   data/plant_diseases/
   ├── Augmented Data/
   │   ├── Cashew/
   │   │   ├── anthracnose/
   │   │   ├── gumosis/
   │   │   ├── healthy/
   │   │   ├── leaf miner/
   │   │   └── red rust/
   │   ├── Cassava/
   │   │   ├── bacterial blight/
   │   │   ├── brown spot/
   │   │   ├── green mite/
   │   │   ├── healthy/
   │   │   └── mosaic/
   │   ├── Maize/
   │   │   ├── fall armyworm/
   │   │   ├── grasshopper/
   │   │   ├── healthy/
   │   │   ├── leaf beetle/
   │   │   ├── leaf blight/
   │   │   ├── leaf spot/
   │   │   └── streak virus/
   │   └── Tomato/
   │       ├── healthy/
   │       ├── leaf blight/
   │       ├── leaf curl/
   │       ├── septoria leaf spot/
   │       └── verticillium wilt/
   └── Raw Data/
       ├── Cashew/
       ├── Cassava/
       ├── Maize/
       └── Tomato/
   ```

### Method 2: Using Kaggle API (Advanced)

1. **Install Kaggle CLI**
   ```bash
   pip install kaggle
   ```

2. **Setup Kaggle Credentials**
   - Go to https://www.kaggle.com/account
   - Click "Create New API Token"
   - Save `kaggle.json` to `~/.kaggle/kaggle.json`
   - Set permissions (Unix/Mac only):
     ```bash
     chmod 600 ~/.kaggle/kaggle.json
     ```

3. **Download Dataset**
   ```bash
   # Download
   kaggle datasets download -d shawontmsez/ccmt-multi-crop-plant-disease-detection-dataset
   
   # Unzip to project directory
   unzip ccmt-multi-crop-plant-disease-detection-dataset.zip -d data/plant_diseases
   
   # Clean up
   rm ccmt-multi-crop-plant-disease-detection-dataset.zip
   ```

## 🚀 Training the Model

### Prerequisites

1. **Check Dataset**
   ```bash
   python scripts/download_dataset_instructions.py
   ```
   This will verify if the dataset is correctly placed.

2. **System Requirements**
   - Python 3.8+
   - TensorFlow 2.17+
   - GPU recommended (training takes 3-4 hours on GPU, much longer on CPU)
   - 16GB+ RAM
   - ~10GB free disk space

### Start Training

```bash
# Activate virtual environment
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Run training script
cd ..
python scripts/train_plant_disease_model.py
```

### Training Configuration

The training script uses the following configuration:
- **Image Size**: 128×128 pixels
- **Batch Size**: 128
- **Epochs**: 50 (with early stopping)
- **Optimizer**: Adam (learning rate: 0.001)
- **Architecture**: Custom CNN (4 conv blocks + dense layers)

### Expected Results

- **Training Time**: 3-4 hours on GPU P100
- **Test Accuracy**: 93-95%
- **Model Size**: ~200MB
- **GPU Memory**: ~12GB required (reduce batch size if needed)

### Output Files

After training completes, you'll find:
```
backend/saved_models/
├── plant_disease_model.keras          # Final trained model
├── plant_disease_best.keras           # Best model during training
├── plant_disease_classes.json         # List of disease classes
├── training_history.png               # Training/validation curves
└── confusion_matrix.png               # Confusion matrix visualization
```

## 🔧 Using the Trained Model

### Update API

The backend API will automatically load the trained model. Restart the backend:

```bash
cd backend
source venv/bin/activate
python app.py
```

### Test via Web Interface

1. Start both backend and frontend
2. Navigate to "Plant Disease Detection" tab
3. Upload a plant image
4. View detection results with:
   - Detected crop
   - Disease name
   - Confidence score
   - Top 3 predictions

### Test via API (curl)

```bash
curl -X POST http://localhost:5001/api/disease-recognition \
  -F "image=@path/to/plant_image.jpg"
```

## 📊 Model Performance

Expected performance metrics:
- **Overall Accuracy**: 93-95%
- **Macro F1-Score**: 0.94+
- **Weighted F1-Score**: 0.95+

Per-crop performance varies based on:
- Number of disease classes per crop
- Class balance
- Image quality

## 💡 Tips & Troubleshooting

### GPU Out of Memory
```python
# In train_plant_disease_model.py, reduce batch size:
BATCH_SIZE = 64  # or 32
```

### Slow Training on CPU
- Training on CPU can take 12+ hours
- Consider using Google Colab (free GPU) or Kaggle Notebooks

### Low Accuracy
- Ensure dataset is correctly extracted
- Check for corrupted images
- Try training for more epochs
- Experiment with different learning rates

### Import Errors
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

## 📚 Additional Resources

- [Original Dataset on Kaggle](https://www.kaggle.com/datasets/shawontmsez/ccmt-multi-crop-plant-disease-detection-dataset)
- [TensorFlow Documentation](https://www.tensorflow.org/)
- [Keras CNN Guide](https://keras.io/examples/vision/)

## 🎓 Citation

If you use this dataset in your research, please cite:

```bibtex
@dataset{ccmt_plant_disease_2024,
  title={CCMT Multi-Crop Plant Disease Detection Dataset},
  author={Shawon Barman},
  year={2024},
  publisher={Kaggle},
  howpublished={\url{https://www.kaggle.com/datasets/shawontmsez/ccmt-multi-crop-plant-disease-detection-dataset}}
}
```

## 🆘 Support

For issues or questions:
1. Check this README
2. Review training logs
3. Check GitHub Issues (if applicable)
4. Contact project maintainers

---

**Happy Training! 🌱🔬**
