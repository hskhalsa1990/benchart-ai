from __future__ import annotations
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import accuracy_score, mean_absolute_error, mean_squared_error, r2_score


def train_tabular_model(rows: list[dict], target: str, task: str = "regression", test_size: float = 0.25, random_state: int = 42):
    frame = pd.DataFrame(rows)
    if target not in frame.columns:
        raise ValueError(f"Target column '{target}' was not found")
    frame = frame.dropna(subset=[target])
    if len(frame) < 8:
        raise ValueError("At least 8 rows with a target value are required")
    X, y = frame.drop(columns=[target]), frame[target]
    if X.empty:
        raise ValueError("At least one feature column is required")
    if task not in {"regression", "classification"}:
        raise ValueError("task must be regression or classification")
    if task == "classification" and y.nunique() < 2:
        raise ValueError("Classification requires at least two target classes")
    numeric = X.select_dtypes(include="number").columns.tolist()
    categorical = [c for c in X.columns if c not in numeric]
    transformers = []
    if numeric:
        transformers.append(("num", SimpleImputer(strategy="median"), numeric))
    if categorical:
        transformers.append(("cat", Pipeline([("imputer", SimpleImputer(strategy="most_frequent")), ("onehot", OneHotEncoder(handle_unknown="ignore"))]), categorical))
    pre = ColumnTransformer(transformers)
    stratify = y if task == "classification" and y.value_counts().min() >= 2 else None
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state, stratify=stratify)
    model = RandomForestRegressor(n_estimators=150, random_state=random_state) if task == "regression" else RandomForestClassifier(n_estimators=150, random_state=random_state)
    pipe = Pipeline([("preprocess", pre), ("model", model)])
    pipe.fit(X_train, y_train)
    pred = pipe.predict(X_test)
    metrics = ({"mae":float(mean_absolute_error(y_test,pred)), "rmse":float(mean_squared_error(y_test,pred)**0.5), "r2":float(r2_score(y_test,pred))} if task == "regression" else {"accuracy":float(accuracy_score(y_test,pred))})
    return {"task":task, "target":target, "rows_used":int(len(frame)), "train_rows":int(len(X_train)), "test_rows":int(len(X_test)), "features":X.columns.tolist(), "metrics":metrics,
            "model":"RandomForest", "note":"Model is trained in-memory for this request; it is not persisted to disk."}
