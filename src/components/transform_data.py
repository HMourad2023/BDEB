import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
import yaml
import os
import pickle

def log_transform(x):
    return np.log1p(x)

def load_params():
    with open('params.yaml', 'r') as f:
        return yaml.safe_load(f)

def encode_categorical_columns(df, cat_columns):
    label_encoders = {}
    
    for col in cat_columns:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        label_encoders[col] = le  # Sauvegarder le LabelEncoder pour chaque colonne
    
    return df, label_encoders

def remove_unwanted_columns(df):
    # Supprimer les colonnes indésirables comme "Unnamed: 0"
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    return df

def transform_data(X_train_path, X_test_path, y_train_path, y_test_path, transformed_data_paths, label_encoders_path):
    # Chargement des données
    X_train = pd.read_csv(X_train_path)
    X_test = pd.read_csv(X_test_path)
    y_train = pd.read_csv(y_train_path)
    y_test = pd.read_csv(y_test_path)

    # Nettoyage des données pour enlever les colonnes indésirables
    X_train = remove_unwanted_columns(X_train)
    X_test = remove_unwanted_columns(X_test)
    y_train = remove_unwanted_columns(y_train)
    y_test = remove_unwanted_columns(y_test)

    cat_columns = X_train.select_dtypes(include='object').columns  # Cols à encoder

    X_train['DISTANCE'] = log_transform(X_train['DISTANCE'])
    X_test['DISTANCE'] = log_transform(X_test['DISTANCE'])

    X_train, encoders = encode_categorical_columns(X_train, cat_columns)
    X_test, encoders = encode_categorical_columns(X_test, cat_columns)

    for col in y_train.columns:
        y_train[col] = log_transform(y_train[col])

    for col in y_test.columns:
        y_test[col] = log_transform(y_test[col])

    # Sauvegarde des données transformées
    X_train.to_csv(transformed_data_paths['X_train_transformed'], index=False)
    X_test.to_csv(transformed_data_paths['X_test_transformed'], index=False)
    y_train.to_csv(transformed_data_paths['y_train_transformed'], index=False)
    y_test.to_csv(transformed_data_paths['y_test_transformed'], index=False)

    # Sauvegarde des transformateurs
    with open(label_encoders_path, 'wb') as f:
        pickle.dump(encoders, f)

if __name__ == "__main__":
    # Chargement des paramètres depuis le fichier YAML
    params = load_params()
    splitted_data_paths = params['data']['splitted_data']
    transformed_data_paths = params['data']['transformed_data']
    label_encoders_path = params['model']['label_encoders_path']
    
    # Création des répertoires si nécessaire
    os.makedirs(os.path.dirname(transformed_data_paths['X_train_transformed']), exist_ok=True)
    os.makedirs(os.path.dirname(transformed_data_paths['X_test_transformed']), exist_ok=True)
    os.makedirs(os.path.dirname(transformed_data_paths['y_train_transformed']), exist_ok=True)
    os.makedirs(os.path.dirname(transformed_data_paths['y_test_transformed']), exist_ok=True)

    # Transformation des données
    transform_data(splitted_data_paths['X_train'], splitted_data_paths['X_test'],
                   splitted_data_paths['y_train'], splitted_data_paths['y_test'],
                   transformed_data_paths, label_encoders_path)
