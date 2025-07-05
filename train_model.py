import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import joblib

# Create sample data based on the notebook structure
np.random.seed(42)
n_samples = 1000

# Generate synthetic data similar to the GHG emission dataset
data = {
    'Substance': np.random.choice(['carbon dioxide', 'methane', 'nitrous oxide', 'other gases'], n_samples),
    'Unit': np.random.choice(['kg/2018 USD, purchaser price', 'kg CO2e/2018 USD, purchaser price'], n_samples),
    'Supply Chain Emission Factors without Margins': np.random.exponential(0.1, n_samples),
    'Margins of Supply Chain Emission Factors': np.random.exponential(0.02, n_samples),
    'DQ ReliabilityScore of Factors without Margins': np.random.choice([2, 3, 4], n_samples),
    'DQ TemporalCorrelation of Factors without Margins': np.random.choice([2, 3], n_samples),
    'DQ GeographicalCorrelation of Factors without Margins': np.ones(n_samples),
    'DQ TechnologicalCorrelation of Factors without Margins': np.random.choice([1, 2, 3, 4, 5], n_samples),
    'DQ DataCollection of Factors without Margins': np.ones(n_samples)
}

df = pd.DataFrame(data)

# Create target variable (with margins)
df['Supply Chain Emission Factors with Margins'] = (
    df['Supply Chain Emission Factors without Margins'] + 
    df['Margins of Supply Chain Emission Factors'] +
    np.random.normal(0, 0.01, n_samples)
)

# Prepare features
le_substance = LabelEncoder()
le_unit = LabelEncoder()

df['Substance_encoded'] = le_substance.fit_transform(df['Substance'])
df['Unit_encoded'] = le_unit.fit_transform(df['Unit'])

# Feature columns
feature_cols = [
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

X = df[feature_cols]
y = df['Supply Chain Emission Factors with Margins']

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train_scaled, y_train)

# Evaluate
y_pred = model.predict(X_test_scaled)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Model Performance:")
print(f"MSE: {mse:.6f}")
print(f"R²: {r2:.4f}")

# Save model and scaler
joblib.dump(model, 'rf_model.pkl')
joblib.dump(scaler, 'rf_scaler.pkl')

# Save label encoders
joblib.dump(le_substance, 'substance_encoder.pkl')
joblib.dump(le_unit, 'unit_encoder.pkl')

print("Model and encoders saved successfully!")