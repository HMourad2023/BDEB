import pandas as pd
import os
import yaml

def load_params():
    with open('params.yaml', 'r') as f:
        return yaml.safe_load(f)

def load_selected_features(file_path):
    with open(file_path, 'r') as file:
        # Lire les lignes du fichier et supprimer les espaces blancs
        selected_features = [line.strip() for line in file.readlines()]
    return selected_features

def select_features(X_train_path, X_test_path, selected_features_file, selected_features_path_train, selected_features_path_test):
    # Chargement des données
    X_train = pd.read_csv(X_train_path)
    X_test = pd.read_csv(X_test_path)
    
    # Chargement des caractéristiques sélectionnées depuis le fichier texte
    selected_features = load_selected_features(selected_features_file)
    
    # Sélection des caractéristiques dans les données
    X_train_selected = X_train[selected_features]
    X_test_selected = X_test[selected_features]
    
    # Sauvegarde des caractéristiques sélectionnées
    X_train_selected.to_csv(selected_features_path_train, index=False)
    X_test_selected.to_csv(selected_features_path_test, index=False)

if __name__ == "__main__":
    # Chargement des paramètres depuis le fichier YAML
    params = load_params()
    X_train_path = params['data']['transformed_data']['X_train_transformed']
    X_test_path = params['data']['transformed_data']['X_test_transformed']
    selected_features_file = params['data']['selected_features']['file']  # Chemin vers le fichier texte des caractéristiques sélectionnées
    selected_features_path_train = params['data']['selected_features']['X_train']
    selected_features_path_test = params['data']['selected_features']['X_test']
    
    # Création des répertoires si nécessaire
    os.makedirs(os.path.dirname(selected_features_path_train), exist_ok=True)
    
    # Sélection et sauvegarde des caractéristiques
    select_features(X_train_path, X_test_path, selected_features_file, selected_features_path_train, selected_features_path_test)


