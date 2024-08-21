import pandas as pd
import os
import yaml

def load_params():
    with open('params.yaml', 'r') as f:
        return yaml.safe_load(f)

def prepare_data(external_data_path):
    data = pd.read_csv(external_data_path)
    data.columns = data.columns.str.strip()

    colonnes_avec_ID = [col for col in data.columns if 'ID' in col]
    data.drop(columns=colonnes_avec_ID, axis=1, inplace=True)
    data.drop(columns=[
        'UNIQUE_CARRIER_NAME', 'UNIQUE_CARRIER_ENTITY', 'CARRIER_NAME',
        'ORIGIN_CITY_NAME', 'ORIGIN_COUNTRY_NAME', 'DEST_CITY_NAME', 'DEST_COUNTRY_NAME'
    ], axis=1, inplace=True)

    # Conversion des colonnes catégorielles en objets
    cat_columns = ['CARRIER_GROUP', 'CARRIER_GROUP_NEW', 'ORIGIN_WAC', 'DEST_WAC']
    data[cat_columns] = data[cat_columns].astype(object)

    # Suppression des lignes avec PASSENGERS, FREIGHT, et MAIL tous égaux à 0
    lignes_zero_valeurs = data[
        (data['PASSENGERS'] == 0) & (data['FREIGHT'] == 0) & (data['MAIL'] == 0)
    ].index
    data.drop(lignes_zero_valeurs, inplace=True)

    # Suppression des valeurs manquantes
    data.dropna(inplace=True)
    data.reset_index(drop=True, inplace=True)

    return data

def save_prepared_data(data, prepared_data_path):
    os.makedirs(os.path.dirname(prepared_data_path), exist_ok=True)
    data.to_csv(prepared_data_path, index=False)

if __name__ == "__main__":
    params = load_params()
    external_data_path = params['data']['external_data']
    prepared_data_path = params['data']['prepared_data']

    prepared_data = prepare_data(external_data_path)
    save_prepared_data(prepared_data, prepared_data_path)
