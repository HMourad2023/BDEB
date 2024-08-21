import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s:')

list_of_files = [
  "src/__init__.py",
  "src/components/__init__.py",
  "src/components/load_data.py",
  "src/components/prepare_data.py",
  "src/components/split_data.py",
  "src/components/features.py",
  "src/components/transform_data.py",
  "src/components/train_and_log_model.py",
  "src/pipeline/__init__.py",
  "src/pipeline/prediction_pipeline.py",
  "visualizations/.gitkeep",
  "images/.gitkeep",
  "params.yaml",
  "requirements.txt",
  "setup.py",
  "notebooks/analysis.ipynb",
  "notebooks/experiments.ipynb",
  "models/.gitkeep",
  "metrics/.gitkeep",
  "selected_features/.gitkeep",
  "app.py",
  "data/external/.gitkeep",
  ".github/workflows/mlops.yaml"
]

for file in list_of_files:
  file_path = Path(file)
  file_path.parent.mkdir(parents=True, exist_ok=True)
  if not file_path.exists():
      file_path.touch()
      logging.info(f"Créé : {file_path}")
  else:
      logging.info(f"Le fichier existe déjà : {file_path}")