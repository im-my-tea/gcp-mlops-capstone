import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score
import joblib

# 1. Load Data
print("Loading data...")
df = pd.read_csv('data.csv')


# Clean column names
df.columns = df.columns.str.strip().str.replace('"', '')

print(f"Columns found: {df.columns.tolist()}") # This will show us what Pandas actually sees


# 2. Preprocessing
df = df.drop(columns=['id', 'Unnamed: 32'], errors='ignore')

# Encode Target: M (Malignant) -> 1, B (Benign) -> 0
# NOTE: Ensure the column name matches exactly what was printed above
df['diagnosis'] = df['diagnosis'].map({'M': 1, 'B': 0})

# Split Features (X) and Target (y)
X = df.drop(columns=['diagnosis'])
y = df['diagnosis']

# 3. Scaling (Critical for Neural Networks)
print("Scaling features...")
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 4. Train/Test Split
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# --- Model 1: Logistic Regression ---
print("\nTraining Logistic Regression...")
lr_model = LogisticRegression()
lr_model.fit(X_train, y_train)
y_pred_lr = lr_model.predict(X_test)
print(f"Logistic Regression Accuracy: {accuracy_score(y_test, y_pred_lr):.4f}")

# --- Model 2: Neural Network (MLP) ---
# Simulating a basic SNN using Sklearn's MLPClassifier
print("\nTraining Neural Network...")
nn_model = MLPClassifier(hidden_layer_sizes=(16, 8), max_iter=1000, random_state=42)
nn_model.fit(X_train, y_train)
y_pred_nn = nn_model.predict(X_test)
print(f"Neural Network Accuracy: {accuracy_score(y_test, y_pred_nn):.4f}")

# 5. Save Artifacts
print("\nSaving artifacts...")
joblib.dump(lr_model, 'app/models/logistic_model.pkl')
joblib.dump(nn_model, 'app/models/neural_net_model.pkl')
joblib.dump(scaler, 'app/models/scaler.pkl')

print("DONE. Models and Scaler saved to app/models/")
