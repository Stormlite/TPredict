# import sys
# import os
# import joblib
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.metrics import accuracy_score, classification_report

# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# import src.ingest as ingest
# import src.preprocess as preprocess

# def train_model(X_train, y_train) -> RandomForestClassifier:
#     """Trains the brain on rankings, H2H, and recent forms."""
#     model = RandomForestClassifier(n_estimators=100, max_depth=8, random_state=42)
#     model.fit(X_train, y_train)
#     return model

# def evaluate_model(model, X_test, y_test) -> float:
#     """Prints diagnostic precision reports."""
#     preds = model.predict(X_test)
#     acc = accuracy_score(y_test, preds)
#     print(f"\n🚀 Enhanced Model Accuracy: {acc:.4f}")
#     print(classification_report(y_test, preds, zero_division=0))
#     return float(acc)

# if __name__ == "__main__":
#     # Ingests multi-year datasets automatically
#     df_raw = ingest.download_historical_data(2022, 2026)
#     df_clean = preprocess.clean_matches(df_raw)
#     df_features = preprocess.engineer_features(df_clean)
#     X_train, X_test, y_train, y_test = preprocess.split_data(df_features)
    
#     model = train_model(X_train, y_train)
#     evaluate_model(model, X_test, y_test)
    
#     # Track and register the columns required by the model
#     model.feature_names_in_ = list(X_train.columns)
    
#     os.makedirs("models", exist_ok=True)
#     joblib.dump(model, "models/rf_model.pkl")
#     print("✅ Advanced model successfully saved to models/rf_model.pkl")

import sys
import os
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import src.ingest as ingest
import src.preprocess as preprocess

def train_model(X_train, y_train) -> RandomForestClassifier:
    """Trains the brain on rankings, H2H, and recent forms."""
    model = RandomForestClassifier(n_estimators=100, max_depth=8, random_state=42)
    model.fit(X_train, y_train)
    return model

def evaluate_model(model, X_test, y_test) -> float:
    """Prints diagnostic precision reports."""
    preds = model.predict(X_test)
    acc = accuracy_score(y_test, preds)
    print(f"\n🚀 Enhanced Model Accuracy: {acc:.4f}")
    print(classification_report(y_test, preds, zero_division=0))
    return float(acc)

if __name__ == "__main__":
    # FIXED: Bound historical tracking from 2022 to 2025 since 2026 is currently unreleased
    df_raw = ingest.download_historical_data(2022, 2025)
    df_clean = preprocess.clean_matches(df_raw)
    df_features = preprocess.engineer_features(df_clean)
    X_train, X_test, y_train, y_test = preprocess.split_data(df_features)
    
    model = train_model(X_train, y_train)
    evaluate_model(model, X_test, y_test)
    
    # Track and register the columns required by the model
    model.feature_names_in_ = list(X_train.columns)
    
    os.makedirs("models", exist_ok=True)
    joblib.dump(model, "models/rf_model.pkl")
    print("✅ Advanced model successfully saved to models/rf_model.pkl")
