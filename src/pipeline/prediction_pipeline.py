import pandas as pd
import joblib
import numpy as np
from sklearn.preprocessing import LabelEncoder
import mlflow
from mlflow.tracking import MlflowClient

def load_model(filepath):
    """Charger le modèle depuis un fichier."""
    return joblib.load(filepath)

def load_preprocessor(filepath):
    """Charger le pr.processeur depuis un fichier."""
    return joblib.load(filepath)

def predict(df_new, model):
    predictions = model.predict(df_new)
    return predictions