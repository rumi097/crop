"""
Instructions for Downloading CCMT Plant Disease Dataset

Dataset: CCMT Multi-Crop Plant Disease Detection Dataset
Source: https://www.kaggle.com/datasets/shawontmsez/ccmt-multi-crop-plant-disease-detection-dataset
Size: ~8 GB
Images: 130,378
"""

import os
import sys

def print_instructions():
    """Print download instructions"""
    
    print("\n" + "=" * 70)
    print("CCMT PLANT DISEASE DATASET - DOWNLOAD INSTRUCTIONS")
    print("=" * 70)
    
    print("\n📦 Dataset Information:")
    print("   Name: CCMT Multi-Crop Plant Disease Detection Dataset")
    print("   URL: https://www.kaggle.com/datasets/shawontmsez/ccmt-multi-crop-plant-disease-detection-dataset")
    print("   Size: ~8 GB")
    print("   Images: 130,378")
    print("   Crops: Cashew, Cassava, Maize, Tomato")
    print("   Classes: 22 disease types")
    
    print("\n" + "=" * 70)
    print("METHOD 1: Manual Download (Recommended)")
    print("=" * 70)
    
    print("\n1️⃣ Go to Kaggle:")
    print("   https://www.kaggle.com/datasets/shawontmsez/ccmt-multi-crop-plant-disease-detection-dataset")
    
    print("\n2️⃣ Click 'Download' button (requires Kaggle account)")
    
    print("\n3️⃣ Extract the downloaded ZIP file:")
    print("   - The ZIP file will be named something like:")
    print("     'ccmt-multi-crop-plant-disease-detection-dataset.zip'")
    
    print("\n4️⃣ Move the extracted 'data' folder to your project:")
    target_path = os.path.abspath('../data/plant_diseases')
    print(f"   Target location: {target_path}")
    
    print("\n5️⃣ Verify the folder structure:")
    print("   data/plant_diseases/")
    print("   ├── Augmented Data/")
    print("   │   ├── Cashew/")
    print("   │   │   ├── anthracnose/")
    print("   │   │   ├── gumosis/")
    print("   │   │   ├── healthy/")
    print("   │   │   ├── leaf miner/")
    print("   │   │   └── red rust/")
    print("   │   ├── Cassava/")
    print("   │   │   ├── bacterial blight/")
    print("   │   │   ├── brown spot/")
    print("   │   │   ├── green mite/")
    print("   │   │   ├── healthy/")
    print("   │   │   └── mosaic/")
    print("   │   ├── Maize/")
    print("   │   │   ├── fall armyworm/")
    print("   │   │   ├── grasshopper/")
    print("   │   │   ├── healthy/")
    print("   │   │   ├── leaf beetle/")
    print("   │   │   ├── leaf blight/")
    print("   │   │   ├── leaf spot/")
    print("   │   │   └── streak virus/")
    print("   │   └── Tomato/")
    print("   │       ├── healthy/")
    print("   │       ├── leaf blight/")
    print("   │       ├── leaf curl/")
    print("   │       ├── septoria leaf spot/")
    print("   │       └── verticillium wilt/")
    print("   └── Raw Data/")
    print("       ├── Cashew/")
    print("       ├── Cassava/")
    print("       ├── Maize/")
    print("       └── Tomato/")
    
    print("\n" + "=" * 70)
    print("METHOD 2: Using Kaggle API (Advanced)")
    print("=" * 70)
    
    print("\n1️⃣ Install Kaggle API:")
    print("   pip install kaggle")
    
    print("\n2️⃣ Set up Kaggle API credentials:")
    print("   - Go to https://www.kaggle.com/account")
    print("   - Click 'Create New API Token'")
    print("   - Save kaggle.json to ~/.kaggle/kaggle.json")
    print("   - On Unix: chmod 600 ~/.kaggle/kaggle.json")
    
    print("\n3️⃣ Download dataset using command:")
    print("   kaggle datasets download -d shawontmsez/ccmt-multi-crop-plant-disease-detection-dataset")
    
    print("\n4️⃣ Unzip the dataset:")
    print("   unzip ccmt-multi-crop-plant-disease-detection-dataset.zip -d ../data/plant_diseases")
    
    print("\n" + "=" * 70)
    print("AFTER DOWNLOADING")
    print("=" * 70)
    
    print("\nOnce the dataset is downloaded and extracted, run:")
    print("   python scripts/train_plant_disease_model.py")
    
    print("\n" + "=" * 70)
    print("TIPS")
    print("=" * 70)
    
    print("\n💡 Training Tips:")
    print("   - Training will take 3-4 hours on GPU")
    print("   - Expected accuracy: 93-95%")
    print("   - Requires ~12GB GPU memory (reduce batch size if needed)")
    print("   - Model size: ~200MB")
    
    print("\n💡 System Requirements:")
    print("   - Free disk space: ~10GB")
    print("   - RAM: 16GB+ recommended")
    print("   - GPU: Highly recommended (NVIDIA with CUDA)")
    
    print("\n" + "=" * 70)


if __name__ == '__main__':
    print_instructions()
    
    # Check if dataset exists
    data_path = '../data/plant_diseases'
    if os.path.exists(data_path):
        print("\n✅ Dataset directory found!")
        
        # Check for required folders
        aug_path = os.path.join(data_path, 'Augmented Data')
        raw_path = os.path.join(data_path, 'Raw Data')
        
        if os.path.exists(aug_path) and os.path.exists(raw_path):
            print("✅ Augmented Data and Raw Data folders found!")
            print("\n🚀 You're ready to train! Run:")
            print("   python scripts/train_plant_disease_model.py")
        else:
            print("⚠️  Dataset directory exists but folders are incomplete")
            print("   Please check the folder structure above")
    else:
        print("\n❌ Dataset not found. Please follow the instructions above.")
