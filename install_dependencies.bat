@echo off
echo Installing required dependencies for GHG Emission Prediction App...
echo.

pip install -r requirements.txt

echo.
echo Installation complete!
echo Run the app with: streamlit run app.py
pause