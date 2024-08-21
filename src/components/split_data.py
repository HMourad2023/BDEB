import pandas as pd
from sklearn.model_selection import train_test_split
import os
import yaml

def load_params():
    with open('params.yaml', 'r') as f:
        return yaml.safe_load(f)

def split_data(prepared_data_path, test_size):
    prepared_data = pd.read_csv(prepared_data_path)
    X = prepared_data.drop(columns=["PASSENGERS", "FREIGHT", "MAIL"])
    y = prepared_data[["PASSENGERS", "FREIGHT", "MAIL"]]
    
    return train_test_split(X, y, test_size=test_size, random_state=42)

def save_splitted_data(X_train, X_test, y_train, y_test, X_train_path, X_test_path, y_train_path, y_test_path):
    os.makedirs(os.path.dirname(X_train_path), exist_ok=True)
    X_train.to_csv(X_train_path, index=False)
    X_test.to_csv(X_test_path, index=False)
    y_train.to_csv(y_train_path, index=False)
    y_test.to_csv(y_test_path, index=False)

if __name__ == "__main__":
    params = load_params()
    prepared_data_path = params['data']['prepared_data']
    splitted_data_paths = params['data']['splitted_data']
    test_size = params['processing']['split_data']['test_size']

    X_train, X_test, y_train, y_test = split_data(prepared_data_path, test_size)
    save_splitted_data(X_train, X_test, y_train, y_test,
                       splitted_data_paths['X_train'], splitted_data_paths['X_test'],
                       splitted_data_paths['y_train'], splitted_data_paths['y_test'])
