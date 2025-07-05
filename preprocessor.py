import pandas as pd
import joblib

def preprocess_input(input_df):
    """
    Preprocess input data for the GHG emission prediction model
    """
    # Create a copy to avoid modifying the original
    df = input_df.copy()
    
    try:
        # Load encoders
        substance_encoder = joblib.load('substance_encoder.pkl')
        unit_encoder = joblib.load('unit_encoder.pkl')
        
        # Encode categorical variables
        df['Substance_encoded'] = substance_encoder.transform(df['Substance'])
        df['Unit_encoded'] = unit_encoder.transform(df['Unit'])
    except:
        # Fallback to manual encoding if encoders not found
        substance_mapping = {
            'carbon dioxide': 0,
            'methane': 1, 
            'nitrous oxide': 2,
            'other gases': 3
        }
        unit_mapping = {
            'kg/2018 USD, purchaser price': 0,
            'kg CO2e/2018 USD, purchaser price': 1
        }
        df['Substance_encoded'] = df['Substance'].map(substance_mapping).fillna(0)
        df['Unit_encoded'] = df['Unit'].map(unit_mapping).fillna(0)
    
    # Select and order features for model input
    feature_columns = [
        'Substance_encoded',
        'Unit_encoded',
        'Supply Chain Emission Factors without Margins',
        'Margins of Supply Chain Emission Factors',
        'DQ ReliabilityScore of Factors without Margins',
        'DQ TemporalCorrelation of Factors without Margins',
        'DQ GeographicalCorrelation of Factors without Margins',
        'DQ TechnologicalCorrelation of Factors without Margins',
        'DQ DataCollection of Factors without Margins'
    ]
    
    return df[feature_columns]