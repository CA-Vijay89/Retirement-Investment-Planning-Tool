import pandas as pd
import numpy as np
import joblib
import os
from tensorflow.keras.models import load_model

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model = load_model(
    os.path.join(BASE_DIR, "risk_profile_model_tf.h5")
)

preprocessor = joblib.load(
    os.path.join(BASE_DIR, "risk_preprocessor.pkl")
)

label_encoder = joblib.load(
    os.path.join(BASE_DIR, "risk_label_encoder.pkl")
)

def predict_risk_profile(age, gender, education, field):
    user_df = pd.DataFrame({
        "age": [age],
        "gender": [gender],
        "education": [education],
        "field": [field]
    })

    processed = preprocessor.transform(user_df)
    probs = model.predict(processed)
    pred_class = np.argmax(probs, axis=1)[0]

    return label_encoder.inverse_transform([pred_class])[0]
