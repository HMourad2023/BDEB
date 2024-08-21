import os
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.ensemble import RandomForestRegressor, ExtraTreesRegressor
from sklearn.metrics import mean_squared_error, r2_score
import mlflow
import mlflow.sklearn
import yaml
import pandas as pd
import joblib  # Pour sauvegarder le modèle localement

def load_params():
    with open('params.yaml', 'r') as f:
        return yaml.safe_load(f)

def train_and_log_model(model_name, model, X_train, X_test, y_train, y_test, local_model_path, metrics_path):
    with mlflow.start_run(run_name=model_name):
        # Entraînement du modèle
        model.fit(X_train, y_train)
        predictions = model.predict(X_test)

        # Calcul des métriques
        mse = mean_squared_error(y_test, predictions)
        rmse = np.sqrt(mse)
        r2 = r2_score(y_test, predictions)

        # Logging des paramètres et métriques
        mlflow.log_params(model.get_params())
        mlflow.log_metric("mean_squared_error", mse)
        mlflow.log_metric("root_mean_squared_error", rmse)
        mlflow.log_metric("R2", r2)

        # Logging du modèle
        mlflow.sklearn.log_model(model, model_name)

        # Sauvegarde du modèle localement
        os.makedirs(os.path.dirname(local_model_path), exist_ok=True)
        joblib.dump(model, local_model_path)

        # Sauvegarde des métriques localement
        os.makedirs(os.path.dirname(metrics_path), exist_ok=True)
        with open(metrics_path, 'w') as f:
            f.write(f"mean_squared_error: {mse}\n")
            f.write(f"root_mean_squared_error: {rmse}\n")
            f.write(f"R2: {r2}\n")

        return r2, rmse

def find_best_model(models, X_train, X_test, y_train, y_test, local_model_path, metrics_path):
    best_model_name = None
    best_r2 = -np.inf
    best_rmse = np.inf

    for model_name, model in models.items():
        print(f"Entraînement du modèle: {model_name}")
        r2, rmse = train_and_log_model(model_name, model, X_train, X_test, y_train, y_test, local_model_path, metrics_path)
        print(f"Modèle: {model_name}, R2: {r2:.4f}, RMSE: {rmse:.4f}")

        if r2 > best_r2 and rmse < best_rmse:
            best_r2 = r2
            best_rmse = rmse
            best_model_name = model_name

    return best_model_name, best_r2, best_rmse

if __name__ == "__main__":
    mlflow.set_tracking_uri("http://localhost:5000")
    mlflow.set_experiment('experience1')

    params = load_params()
    X_train_selected_path = params['data']['selected_features']['X_train']
    X_test_selected_path = params['data']['selected_features']['X_test']
    y_train_transformed_path = params['data']['transformed_data']['y_train_transformed']
    y_test_transformed_path = params['data']['transformed_data']['y_test_transformed']
    local_model_path = params['model']['local_model_path']
    metrics_path = params['model']['metrics_path']

    # Chargement des données
    X_train = pd.read_csv(X_train_selected_path)
    X_test = pd.read_csv(X_test_selected_path)
    y_train = pd.read_csv(y_train_transformed_path).squeeze()  # Utiliser squeeze() pour avoir une série 1D
    y_test = pd.read_csv(y_test_transformed_path).squeeze()

    # Modèles à entraîner
    models = {
        "LinearRegression": LinearRegression(),
        "KNeighborsRegressor": KNeighborsRegressor(),
        "RandomForestRegressor": RandomForestRegressor(),
        "ExtraTreesRegressor": ExtraTreesRegressor()
    }

    # Entraînement et sélection du meilleur modèle
    best_model_name, best_r2, best_rmse = find_best_model(models, X_train, X_test, y_train, y_test, local_model_path, metrics_path)
    print(f"Le meilleur modèle est {best_model_name} avec un R2 de {best_r2:.4f} et un RMSE de {best_rmse:.4f}")
