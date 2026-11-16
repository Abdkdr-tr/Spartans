import os

# Chemins des dossiers et fichiers
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.normpath(os.path.join(BASE_DIR, "..", "database", "spartans.db"))
DATASET_PATH = os.path.join(BASE_DIR, "dataset.csv")

# Paramètres du modèle d'embedding (Option A)
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
# Nombre de textes traités simultanément en parallèle par le modèle d'embedding
BATCH_SIZE = 64
