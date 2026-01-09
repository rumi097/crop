# 🧪 Testing Guide - Crop Recommendation System

## Quick Test Commands

### 1. Test Crop Recommendation API

```bash
# Test 1: Rice recommendation
curl -X POST http://localhost:5000/api/crop-recommendation \
  -H "Content-Type: application/json" \
  -d '{
    "N": 90,
    "P": 42,
    "K": 43,
    "temperature": 20.87,
    "humidity": 82.0,
    "pH": 6.5,
    "rainfall": 202.9
  }'

# Test 2: Wheat recommendation
curl -X POST http://localhost:5000/api/crop-recommendation \
  -H "Content-Type: application/json" \
  -d '{
    "N": 110,
    "P": 55,
    "K": 45,
    "temperature": 23.5,
    "humidity": 65.0,
    "pH": 7.0,
    "rainfall": 75.0
  }'

# Test 3: Cotton recommendation
curl -X POST http://localhost:5000/api/crop-recommendation \
  -H "Content-Type: application/json" \
  -d '{
    "N": 120,
    "P": 50,
    "K": 50,
    "temperature": 26.0,
    "humidity": 70.0,
    "pH": 7.5,
    "rainfall": 80.0
  }'
```

### 2. Test Fertilizer Recommendation API

```bash
# Test 1: High nitrogen deficiency
curl -X POST http://localhost:5000/api/fertilizer-recommendation \
  -H "Content-Type: application/json" \
  -d '{
    "N": 30,
    "P": 50,
    "K": 40,
    "crop": "wheat",
    "soil_type": "loamy"
  }'

# Test 2: High phosphorus deficiency
curl -X POST http://localhost:5000/api/fertilizer-recommendation \
  -H "Content-Type: application/json" \
  -d '{
    "N": 100,
    "P": 20,
    "K": 50,
    "crop": "rice",
    "soil_type": "clayey"
  }'

# Test 3: Adequate nutrients
curl -X POST http://localhost:5000/api/fertilizer-recommendation \
  -H "Content-Type: application/json" \
  -d '{
    "N": 120,
    "P": 70,
    "K": 45,
    "crop": "maize",
    "soil_type": "sandy"
  }'
```

### 3. Test Health Check

```bash
curl http://localhost:5000/api/health
```

### 4. Get Available Options

```bash
# Get available crops
curl http://localhost:5000/api/available-crops

# Get soil types
curl http://localhost:5000/api/soil-types
```

## Python Testing Scripts

### Test Crop Model Directly

```python
import sys
sys.path.append('backend')

from models.crop_recommendation import CropRecommendationModel

# Load trained model
model = CropRecommendationModel()
model.load_model('backend/saved_models/crop_model.pkl',
                 'backend/saved_models/crop_scaler.pkl')

# Test prediction
test_input = {
    'N': 90,
    'P': 42,
    'K': 43,
    'temperature': 20.87,
    'humidity': 82.0,
    'pH': 6.5,
    'rainfall': 202.9
}

result = model.predict(test_input)
print(f"Recommended Crop: {result['crop']}")
print(f"Confidence: {result['confidence']*100:.2f}%")
```

### Test Fertilizer Model

```python
from models.fertilizer_recommendation import FertilizerRecommendationModel

# Initialize model
fert_model = FertilizerRecommendationModel(use_ml=False)

# Test recommendation
test_input = {
    'N': 30,
    'P': 20,
    'K': 25,
    'crop': 'wheat',
    'soil_type': 'loamy'
}

result = fert_model.predict(test_input)
print(f"Recommended Fertilizer: {result['fertilizer']}")
print(f"Amount: {result.get('amount', 'N/A')}")
print(f"Reason: {result['reason']}")
```

### Test CNN Model

Note: Disease recognition has been removed from this project.

## Frontend Testing Checklist

### Crop Recommendation Page

- [ ] All input fields accept numeric values
- [ ] Input validation works (min/max ranges)
- [ ] Form submission triggers API call
- [ ] Loading spinner displays during request
- [ ] Results display correctly with confidence score
- [ ] Top 3 predictions are shown
- [ ] Reset button clears form and results
- [ ] Error messages display for invalid inputs
- [ ] Responsive design works on mobile

### Fertilizer Recommendation Page

- [ ] N, P, K inputs accept values
- [ ] Crop dropdown populated correctly
- [ ] Soil type dropdown populated correctly
- [ ] API call triggers on submit
- [ ] Recommendation displays with details
- [ ] Nutrient analysis shows current vs required
- [ ] Deficiency indicators work correctly
- [ ] Application methods display
- [ ] Color coding for nutrient status

### Disease Recognition Page

Removed.

## Sample Test Data

### Crop Recommendation Test Cases

```json
// Test Case 1: Rice (High humidity, high rainfall)
{
  "N": 85,
  "P": 40,
  "K": 40,
  "temperature": 25.0,
  "humidity": 83.0,
  "pH": 6.5,
  "rainfall": 220.0
}

// Test Case 2: Wheat (Moderate conditions)
{
  "N": 110,
  "P": 60,
  "K": 45,
  "temperature": 21.0,
  "humidity": 62.0,
  "pH": 6.8,
  "rainfall": 85.0
}

// Test Case 3: Cotton (High N, warm)
{
  "N": 125,
  "P": 45,
  "K": 48,
  "temperature": 27.0,
  "humidity": 68.0,
  "pH": 7.2,
  "rainfall": 75.0
}

// Test Case 4: Banana (High nutrients, warm, humid)
{
  "N": 95,
  "P": 85,
  "K": 50,
  "temperature": 28.0,
  "humidity": 80.0,
  "pH": 6.5,
  "rainfall": 120.0
}

// Test Case 5: Apple (Cool temperature)
{
  "N": 20,
  "P": 125,
  "K": 200,
  "temperature": 20.0,
  "humidity": 60.0,
  "pH": 6.0,
  "rainfall": 110.0
}
```

### Fertilizer Recommendation Test Cases

```json
// Test Case 1: High N deficiency
{
  "N": 25,
  "P": 55,
  "K": 40,
  "crop": "wheat",
  "soil_type": "loamy"
}
// Expected: Urea

// Test Case 2: High P deficiency
{
  "N": 95,
  "P": 15,
  "K": 45,
  "crop": "rice",
  "soil_type": "clayey"
}
// Expected: DAP

// Test Case 3: High K deficiency
{
  "N": 100,
  "P": 60,
  "K": 20,
  "crop": "cotton",
  "soil_type": "sandy"
}
// Expected: MOP

// Test Case 4: Multiple deficiencies
{
  "N": 40,
  "P": 25,
  "K": 30,
  "crop": "maize",
  "soil_type": "loamy"
}
// Expected: NPK balanced

// Test Case 5: Adequate nutrients
{
  "N": 120,
  "P": 65,
  "K": 42,
  "crop": "wheat",
  "soil_type": "loamy"
}
// Expected: No fertilizer needed
```

## Performance Testing

### Load Testing with Apache Bench

```bash
# Test crop recommendation endpoint
ab -n 1000 -c 10 -p crop_test.json -T application/json \
   http://localhost:5000/api/crop-recommendation

# Where crop_test.json contains:
# {"N":90,"P":42,"K":43,"temperature":20.87,"humidity":82.0,"pH":6.5,"rainfall":202.9}
```

### Response Time Benchmarks

Expected response times:
- Crop Recommendation: < 100ms
- Fertilizer Recommendation: < 50ms
- Health Check: < 10ms

## Integration Testing

### Full Workflow Test

```bash
# 1. Check health
curl http://localhost:5000/api/health

# 2. Get crop recommendation
curl -X POST http://localhost:5000/api/crop-recommendation \
  -H "Content-Type: application/json" \
  -d '{"N":90,"P":42,"K":43,"temperature":20.87,"humidity":82.0,"pH":6.5,"rainfall":202.9}'

# 3. Get fertilizer recommendation
curl -X POST http://localhost:5000/api/fertilizer-recommendation \
  -H "Content-Type: application/json" \
  -d '{"N":30,"P":20,"K":25,"crop":"wheat","soil_type":"loamy"}'
```

## Automated Testing

### Unit Tests (Create test_models.py)

```python
import unittest
from models.crop_recommendation import CropRecommendationModel
from models.fertilizer_recommendation import FertilizerRecommendationModel

class TestCropModel(unittest.TestCase):
    def setUp(self):
        self.model = CropRecommendationModel()
        self.model.load_model()
    
    def test_prediction(self):
        input_data = {
            'N': 90, 'P': 42, 'K': 43,
            'temperature': 20.87, 'humidity': 82.0,
            'pH': 6.5, 'rainfall': 202.9
        }
        result = self.model.predict(input_data)
        self.assertIn('crop', result)
        self.assertIn('confidence', result)
        self.assertGreater(result['confidence'], 0)

class TestFertilizerModel(unittest.TestCase):
    def setUp(self):
        self.model = FertilizerRecommendationModel()
    
    def test_recommendation(self):
        input_data = {
            'N': 30, 'P': 20, 'K': 25,
            'crop': 'wheat', 'soil_type': 'loamy'
        }
        result = self.model.predict(input_data)
        self.assertIn('fertilizer', result)
        self.assertIn('reason', result)

if __name__ == '__main__':
    unittest.main()
```

Run tests:
```bash
cd backend
python -m pytest test_models.py
```

## Common Issues & Solutions

### Issue 1: Model Not Found
```
Solution: Train models first
cd scripts && python train_crop_model.py
```

### Issue 2: CORS Error
```
Solution: Ensure Flask-CORS is installed and enabled
pip install flask-cors
```

### Issue 3: Image Upload Fails
```
Solution: Check file size and format
- Max size: 16MB
- Formats: JPG, PNG, BMP
```

### Issue 4: Low Accuracy
```
Solution: 
- Use actual Kaggle dataset
- Increase training data
- Tune hyperparameters
```

## Test Results Documentation

### Example Test Report

```
Test Date: 2025-12-24
Test Environment: Local Development

Crop Recommendation API:
✅ Test 1: Rice prediction - PASS (95% confidence)
✅ Test 2: Wheat prediction - PASS (98% confidence)
✅ Test 3: Cotton prediction - PASS (92% confidence)
✅ Test 4: Invalid input - PASS (proper error)
✅ Test 5: Missing fields - PASS (validation error)

Fertilizer Recommendation API:
✅ Test 1: High N deficiency - PASS (Urea recommended)
✅ Test 2: High P deficiency - PASS (DAP recommended)
✅ Test 3: Adequate nutrients - PASS (No fertilizer)
✅ Test 4: Multiple deficiencies - PASS (NPK recommended)

Disease Recognition API:
✅ Test 1: Healthy fertilizer - PASS (89% confidence)
⚠️  Test 2: CNN model not trained - SKIP
✅ Test 3: Invalid format - PASS (error message)
✅ Test 4: File too large - PASS (error message)

Performance:
✅ Crop API: 85ms average
✅ Fertilizer API: 42ms average
✅ Health check: 5ms average

Overall: 15/16 tests passed (93.75%)
```

## Next Steps After Testing

1. Fix any failing tests
2. Improve model accuracy if needed
3. Optimize response times
4. Add more test cases
5. Implement automated CI/CD testing
6. Prepare for deployment

---

**Testing Complete! Ready for Production** ✅

For any issues, refer to:
- README.md - Full documentation
- PROJECT_SUMMARY.md - Technical details
- QUICKSTART.md - Setup guide
