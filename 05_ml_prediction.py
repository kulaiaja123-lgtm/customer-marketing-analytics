# ============================================
# MACHINE LEARNING: PREDIKSI RESPONSE CAMPAIGN
# ============================================

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import joblib

# Load data
df = pd.read_csv('customer_clean.csv')

# ============================================
# 1. SIAPKAN DATA
# ============================================

# Pilih fitur (X) dan target (y)
feature_cols = [
    'Age', 'Income', 'Total_Children', 'Total_Spending',
    'Total_Purchases', 'Recency', 'NumWebPurchases',
    'NumCatalogPurchases', 'NumStorePurchases', 'NumDealsPurchases',
    'NumWebVisitsMonth', 'Complain'
]

X = df[feature_cols]
y = df['Response']  # 1 = respon, 0 = tidak

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print("=" * 50)
print("DATA SPLIT")
print("=" * 50)
print(f"Training: {len(X_train)} samples")
print(f"Testing: {len(X_test)} samples")
print(f"Response rate train: {y_train.mean()*100:.1f}%")
print(f"Response rate test: {y_test.mean()*100:.1f}%")

# ============================================
# 2. TRAIN MODEL
# ============================================

print("\n" + "=" * 50)
print("TRAINING MODEL")
print("=" * 50)

model = RandomForestClassifier(
    n_estimators=100,
    max_depth=10,
    random_state=42,
    class_weight='balanced'  # Handle imbalanced data
)

model.fit(X_train, y_train)

# ============================================
# 3. EVALUASI
# ============================================

print("\n" + "=" * 50)
print("EVALUASI MODEL")
print("=" * 50)

y_pred = model.predict(X_test)

print("\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=['No Response', 'Response']))

# ============================================
# 4. FEATURE IMPORTANCE
# ============================================

print("\n" + "=" * 50)
print("FEATURE IMPORTANCE")
print("=" * 50)

importance = pd.DataFrame({
    'Feature': feature_cols,
    'Importance': model.feature_importances_
}).sort_values('Importance', ascending=False)

print(importance)

# ============================================
# 5. SIMPAN MODEL
# ============================================

joblib.dump(model, 'response_predictor.pkl')
print("\n✅ Model tersimpan: response_predictor.pkl")

# ============================================
# 6. CONTOH PREDIKSI
# ============================================

print("\n" + "=" * 50)
print("CONTOH PREDIKSI")
print("=" * 50)

# Customer baru
new_customer = pd.DataFrame([{
    'Age': 45,
    'Income': 75000,
    'Total_Children': 1,
    'Total_Spending': 1200,
    'Total_Purchases': 15,
    'Recency': 30,
    'NumWebPurchases': 5,
    'NumCatalogPurchases': 8,
    'NumStorePurchases': 2,
    'NumDealsPurchases': 0,
    'NumWebVisitsMonth': 3,
    'Complain': 0
}])

prediction = model.predict(new_customer)
probability = model.predict_proba(new_customer)

print(f"Prediksi: {'AKAN RESPON' if prediction[0] == 1 else 'TIDAK RESPON'}")
print(f"Probabilitas respon: {probability[0][1]*100:.1f}%")