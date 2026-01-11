import pandas as pd
import numpy as np
import joblib
import os
import tensorflow as tf
from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import to_categorical

from sklearn.preprocessing import OneHotEncoder, StandardScaler, LabelEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# -------------------------------------------------
# 1. LOAD DATASET
# -------------------------------------------------
# Update filename if different
data_path = os.path.join(BASE_DIR, "risk_profile_data.csv")
df = pd.read_csv(data_path)

# Features & target
X = df[["age", "gender", "education", "field"]]
y = df["risk_pref"]   # aggressive / moderate / conservative


# ---------------------------------------------
# 2. CREATE PREPROCESSOR & LABEL ENCODER (NEW)
# ---------------------------------------------
num_features = ["age"]
cat_features = ["gender", "education", "field"]

preprocessor = ColumnTransformer(
    transformers=[
        ("num", StandardScaler(), num_features),
        ("cat", OneHotEncoder(handle_unknown="ignore"), cat_features)
    ]
)

X_processed = preprocessor.fit_transform(X)

label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)
y_categorical = to_categorical(y_encoded)

# SAVE PREPROCESSOR & LABEL ENCODER
joblib.dump(
    preprocessor,
    os.path.join(BASE_DIR, "risk_preprocessor.pkl")
)

joblib.dump(
    label_encoder,
    os.path.join(BASE_DIR, "risk_label_encoder.pkl")
)


# -------------------------------------------------
# 3. TRAIN / TEST SPLIT
# -------------------------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X_processed,
    y_categorical,
    test_size=0.2,
    random_state=42
)

# -------------------------------------------------
# 4. BUILD TF-KERAS MODEL (CLEAN)
# -------------------------------------------------
model = tf.keras.Sequential([
    tf.keras.layers.Dense(64, activation="relu", input_shape=(X_train.shape[1],)),
    tf.keras.layers.Dropout(0.3),
    tf.keras.layers.Dense(32, activation="relu"),
    tf.keras.layers.Dense(y_categorical.shape[1], activation="softmax")
])

model.compile(
    optimizer="adam",
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)

# -------------------------------------------------
# 5. TRAIN MODEL
# -------------------------------------------------
history = model.fit(
    X_train,
    y_train,
    validation_data=(X_test, y_test),
    epochs=30,
    batch_size=32,
    verbose=1
)

# -------------------------------------------------
# 6. SAVE TF-COMPATIBLE MODEL
# -------------------------------------------------
model.save(
    os.path.join(BASE_DIR, "risk_profile_model_tf.h5")
)

print("✅ Model retrained and saved successfully")
