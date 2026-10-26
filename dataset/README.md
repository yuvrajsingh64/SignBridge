# ASL Alphabet Dataset

## Source
**ASL Alphabet** by Akash Nagaraj (grassknoted)  
Kaggle: https://www.kaggle.com/datasets/grassknoted/asl-alphabet

## Description
- **87,000+** images across **29 classes**
- **26 ASL alphabet letters** (A–Z) + **3 special classes** (del, nothing, space)
- Each image is **200×200 pixels**, color (RGB)
- ~3,000 images per class

## License
The dataset is available on Kaggle under **CC0: Public Domain** license.

## Download Instructions

### Option 1: Using kagglehub (Recommended)
```bash
pip install kagglehub
python -c "import kagglehub; path = kagglehub.dataset_download('grassknoted/asl-alphabet'); print(f'Downloaded to: {path}')"
```
Then copy the `asl_alphabet_train` directory into this `dataset/` folder.

### Option 2: Manual Download
1. Go to https://www.kaggle.com/datasets/grassknoted/asl-alphabet
2. Click "Download" (requires free Kaggle account)
3. Extract the downloaded ZIP file
4. Place the `asl_alphabet_train` folder here

## Expected Structure After Download
```
dataset/
  asl_alphabet_train/
    asl_alphabet_train/
      A/        (3000 images)
      B/        (3000 images)
      ...
      Z/        (3000 images)
      del/      (3000 images)
      nothing/  (3000 images)
      space/    (3000 images)
  asl_alphabet_test/
    asl_alphabet_test/
      (29 test images, one per class)
```

## Notes on J and Z
- Letters **J** and **Z** in ASL involve motion/tracing
- This dataset represents them with static images (a single frame)
- Model accuracy for J and Z may be lower than for static signs
