# GHG Emission Prediction App

A Streamlit web application for predicting Supply Chain Emission Factors with Margin based on various environmental and operational parameters.

## Quick Start

### Option 1: Automatic Installation (Windows)
1. Double-click `install_dependencies.bat`
2. Run: `streamlit run app.py`

### Option 2: Manual Installation
```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

### Option 3: Demo Mode
```bash
# Run simplified version without dependencies
streamlit run app_simple.py
```

##  Dependencies

- streamlit>=1.28.0
- scikit-learn>=1.3.0
- joblib>=1.3.0
- pandas>=2.0.0
- numpy>=1.24.0

##  Project Structure

```
GHG-EMISSION-PREDICTION/
├── app.py                    # Main application (requires dependencies)
├── app_simple.py            # Demo version (no dependencies)
├── utils/
│   ├── __init__.py
│   └── preprocessor.py      # Data preprocessing functions
├── requirements.txt         # Python dependencies
├── install_dependencies.bat # Windows installer
├── LR_model.pkl            # Trained model
├── scaler (4).pkl          # Data scaler
└── README.md               # This file
```

##  Features

- Interactive web interface
- Real-time predictions
- Input validation
- Results visualization
- Parameter summary display

##  Troubleshooting

If you encounter import errors, ensure all dependencies are installed:
```bash
pip install --upgrade -r requirements.txt
```
