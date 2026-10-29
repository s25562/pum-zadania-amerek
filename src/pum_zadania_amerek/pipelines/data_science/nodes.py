"""
This is a boilerplate pipeline 'data_science'
generated using Kedro 1.7.0
"""

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (accuracy_score, precision_score, recall_score,
                             f1_score, confusion_matrix, ConfusionMatrixDisplay)


# ---------- PREPROCESSING ----------
def prepare_titanic(df: pd.DataFrame, params: dict) -> pd.DataFrame:
    df = df.drop(columns=params["drop_columns"])
    df["Age"] = df["Age"].fillna(df["Age"].median())              # mediana
    df["Embarked"] = df["Embarked"].fillna(df["Embarked"].mode()[0])
    df["Sex"] = df["Sex"].map({"male": 0, "female": 1})
    df = pd.get_dummies(df, columns=["Embarked"], drop_first=True)
    return df


def prepare_orders(df: pd.DataFrame, params: dict) -> pd.DataFrame:
    df = df.drop_duplicates(subset="order_id").copy()

    # ujednolicenie brudnych kategorii: "Wh Tshirt M" -> "White T-Shirt M"
    df["tshirt_category"] = (df["tshirt_category"]
        .str.replace("Wh Tshirt", "White T-Shirt", regex=False)
        .str.replace("Bl Tshirt", "Black T-Shirt", regex=False))

    df["month"] = pd.to_datetime(df["order_date"]).dt.month
    df["big_order"] = (df["tshirt_quantity"] >= params["big_order_threshold"]).astype(int)

    df = df.drop(columns=params["drop_columns"])
    df = pd.get_dummies(df, columns=["tshirt_category"], drop_first=True)
    return df


# ---------- TRENING ----------
def train_model(df: pd.DataFrame, params: dict, target: str):
    X, y = df.drop(columns=[target]), df[target]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=params["test_size"],
        random_state=params["random_state"], stratify=y)

    model = RandomForestClassifier(
        n_estimators=params["n_estimators"], 
        random_state=params["random_state"],
        class_weight=params.get("class_weight"))
    model.fit(X_train, y_train)
    return model, X_test, y_test


# ---------- EWALUACJA ----------
def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    metrics = {
        "accuracy": accuracy_score(y_test, y_pred),
        "precision": precision_score(y_test, y_pred),
        "recall": recall_score(y_test, y_pred),
        "f1": f1_score(y_test, y_pred),
        "confusion_matrix": confusion_matrix(y_test, y_pred).tolist(),
    }
    fig, ax = plt.subplots()
    ConfusionMatrixDisplay.from_predictions(y_test, y_pred, ax=ax)
    return metrics, fig


def train_titanic(df: pd.DataFrame, params: dict):
    return train_model(df, params, target=params["target"])


def train_orders(df: pd.DataFrame, params: dict):
    return train_model(df, params, target="big_order")
