import streamlit as st
import joblib
import numpy as np
import pandas as pd
from utils.preprocessor import preprocess_input

# Load model and scaler with error handling
model_loaded = False
try:
    # Try to load the RandomForest model
    model = joblib.load('rf_model.pkl')
    scaler = joblib.load('rf_scaler.pkl')
    model_loaded = True
    st.success("✅ RandomForest Model loaded successfully!")
except Exception as e:
    try:
        # Fallback to simple compatible model
        model = joblib.load('simple_model.pkl')
        scaler = joblib.load('simple_scaler.pkl')
        model_loaded = True
        st.info("🔄 Using compatible ML model (simplified version)")
    except Exception as e2:
        st.warning("⚠️ Model loading failed. Running in demo mode.")
        model_loaded = False

st.title("Supply Chain Emissions Prediction")
st.markdown("This app predicts Supply Chain Emission Factors with Margin based on various parameters.")

# Input form
with st.form("prediction_form"):
    st.subheader("Input Parameters")
    
    col1, col2 = st.columns(2)
    
    with col1:
        substance = st.selectbox("Substance", ['carbon dioxide', 'methane', 'nitrous oxide', 'other gases'])
        unit = st.selectbox("Unit", ['kg/2018 USD, purchaser price', 'kg CO2e/2018 USD, purchaser price'])
        supply_wo_margin = st.number_input("Supply Chain Emission Factors without Margins", min_value=0.0, value=0.1, step=0.01)
        margin = st.number_input("Margins of Supply Chain Emission Factors", min_value=0.0, value=0.01, step=0.001)
        dq_reliability = st.slider("DQ ReliabilityScore of Factors without Margins", 2, 4, 3)
    
    with col2:
        dq_temporal = st.slider("DQ TemporalCorrelation of Factors without Margins", 2, 3, 3)
        dq_geo = st.number_input("DQ GeographicalCorrelation of Factors without Margins", value=1, disabled=True)
        dq_tech = st.slider("DQ TechnologicalCorrelation of Factors without Margins", 1, 5, 3)
        dq_data = st.number_input("DQ DataCollection of Factors without Margins", value=1, disabled=True)
    
    submitted = st.form_submit_button("Predict", type="primary")
    
    if submitted:
        # Prepare input data
        input_data = {
            'Substance': substance,
            'Unit': unit,
            'Supply Chain Emission Factors without Margins': supply_wo_margin,
            'Margins of Supply Chain Emission Factors': margin,
            'DQ ReliabilityScore of Factors without Margins': dq_reliability,
            'DQ TemporalCorrelation of Factors without Margins': dq_temporal,
            'DQ GeographicalCorrelation of Factors without Margins': dq_geo,
            'DQ TechnologicalCorrelation of Factors without Margins': dq_tech,
            'DQ DataCollection of Factors without Margins': dq_data
        }
        
        if model_loaded:
            try:
                # Use actual model
                input_df = preprocess_input(pd.DataFrame([input_data]))
                input_scaled = scaler.transform(input_df)
                prediction = model.predict(input_scaled)
                st.success(f"🎯 Predicted Supply Chain Emission Factor with Margin: **{prediction[0]:.4f}**")
            except Exception as e:
                st.error(f"Prediction failed: {str(e)}")
                # Fallback to demo prediction
                prediction = supply_wo_margin + margin + (dq_reliability * 0.01) + (dq_tech * 0.005)
                st.info(f"🟡 Demo Prediction: **{prediction:.4f}**")
        else:
            # Demo mode prediction
            prediction = supply_wo_margin + margin + (dq_reliability * 0.01) + (dq_tech * 0.005)
            st.info(f"🟡 Demo Prediction: **{prediction:.4f}**")
        
        # Display input summary
        with st.expander("Input Summary"):
            st.json(input_data)