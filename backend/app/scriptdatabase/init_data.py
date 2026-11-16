import os
import sqlite3
import pandas as pd
import numpy as np
import kagglehub
from sentence_transformers import SentenceTransformer
from config import DB_PATH, EMBEDDING_MODEL_NAME, BATCH_SIZE

def nettoyer_texte_liste(valeur):
    """Nettoie les chaînes de caractères qui ressemblent à des listes (ex: ['Beginner', 'Novice'])."""
    if pd.isna(valeur):
        return ""
    return str(valeur).replace("[", "").replace("]", "").replace("'", "").replace('"', "").replace(",", " ")

def formater_reps(valeur):
    """Formate la colonne 'reps' avant insertion en base.
    D'après la doc du dataset Kaggle, les valeurs négatives sont des durées en secondes (ex: -180 -> '180 sec').
    """
    if pd.isna(valeur):
        return ""
    try:
        num = float(valeur)
        if num < 0:
            return f"{int(abs(num))} sec"
        return str(int(num)) if num.is_integer() else str(num)
    except ValueError:
        return str(valeur).strip()

def executer_etl():
    print("📥 Téléchargement du dataset Kaggle...")
    chemin_dossier = kagglehub.dataset_download("adnanelouardi/600k-fitness-exercise-and-workout-program-dataset")
    
    # Chemin direct vers notre fichier CSV
    chemin_csv = os.path.join(chemin_dossier, "programs_detailed_boostcamp_kaggle.csv")
    print(f"📊 Fichier CSV cible : {chemin_csv}")

    print("🧹 Chargement et nettoyage des données avec Pandas...")
    df = pd.read_csv(chemin_csv)
    
    df['level_propre'] = df['level'].apply(nettoyer_texte_liste)
    df['goal_propre'] = df['goal'].apply(nettoyer_texte_liste)
    df['equipment_propre'] = df['equipment'].apply(nettoyer_texte_liste)
    
    df['title'] = df['title'].fillna('')
    df['description'] = df['description'].fillna('')
    df['exercise_name'] = df['exercise_name'].fillna('')

    # Création du texte combiné pour la vectorisation sémantique des PROGRAMMES
    df['texte_programme'] = (
        "Program: " + df['title'] + ". " +
        "Goal: " + df['goal_propre'] + ". " +
        "Level: " + df['level_propre'] + ". " +
        "Equipment: " + df['equipment_propre'] + ". " +
        "Description: " + df['description']
    )

    print(f"🧠 Chargement du modèle d'embedding ({EMBEDDING_MODEL_NAME})...")
    model = SentenceTransformer(EMBEDDING_MODEL_NAME)

    # On isole les programmes uniques pour ne pas calculer les embeddings de programmes en double
    print("🔍 Extraction et vectorisation des programmes uniques par batchs...")
    df_programmes_uniques = df.drop_duplicates(subset=['title']).copy()
    textes_programmes = df_programmes_uniques['texte_programme'].tolist()

    # Génération des embeddings en batchs (parallélisation CPU optimale)
    embeddings_matrice = model.encode(
        textes_programmes, 
        batch_size=BATCH_SIZE, 
        show_progress_bar=True
    )

    # Création d'un dictionnaire de correspondance : titre_programme -> vecteur en octets (BLOB)
    programmes_embeddings_dict = {}
    for idx, row in df_programmes_uniques.reset_index(drop=True).iterrows():
        titre_prog = row['title']
        # Conversion du vecteur float32 en octets bruts pour SQLite
        vector_bytes = embeddings_matrice[idx].astype(np.float32).tobytes()
        programmes_embeddings_dict[titre_prog] = vector_bytes

    # Création du dossier 'database' si besoin
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    print("💾 Insertion des programmes et des exercices dans la base SQLite...")
    connexion = sqlite3.connect(DB_PATH)
    curseur = connexion.cursor()
    
    # On vide les tables avant de les re-remplir pour repartir sur du propre
    curseur.execute("DELETE FROM program_exercises;")
    curseur.execute("DELETE FROM workout_programs;")

    # Dictionnaires pour stocker les IDs et éviter les doublons
    programmes_enregistres = {}

    # Boucle pour parcourir le DataFrame et remplir les tables relationnelles
    for index, ligne in df.iterrows():
        
        # --- table workout_programs (avec embedding BLOB) ---
        titre_prog = ligne['title']
        if titre_prog not in programmes_enregistres:
            vector_bytes = programmes_embeddings_dict.get(titre_prog)
            curseur.execute("""
                INSERT INTO workout_programs (title, description, target_level, program_goal, required_equipment, embedding_vector)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                titre_prog,
                ligne['description'],
                ligne['level_propre'],
                ligne['goal_propre'],
                ligne['equipment_propre'],
                vector_bytes
            ))
            programmes_enregistres[titre_prog] = curseur.lastrowid
        
        prog_id = programmes_enregistres[titre_prog]

        nom_ex = ligne['exercise_name']
        if nom_ex != '':
            curseur.execute("""
                INSERT INTO program_exercises (program_id, exercise_name, week_number, day_number, set_count, rep_count, intensity_rate)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                prog_id,
                nom_ex,
                ligne['week'],
                ligne['day'],
                ligne['sets'],
                formater_reps(ligne['reps']),
                ligne['intensity']
            ))


    connexion.commit()

    # Vérifications 
    curseur.execute("SELECT COUNT(*) FROM workout_programs;")
    nb_programmes = curseur.fetchone()[0]

    curseur.execute("SELECT COUNT(*) FROM program_exercises;")
    nb_exercices_programmes = curseur.fetchone()[0]

    connexion.close()

    print(f"\n✅ ETL et peuplement terminés avec succès !")
    print(f"   - Programmes insérés (avec embeddings) : {nb_programmes}")
    print(f"   - Exercices programmés insérés         : {nb_exercices_programmes}")

if __name__ == "__main__":
    executer_etl()