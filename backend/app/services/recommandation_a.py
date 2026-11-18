"""
Module de recommandation - Option A (approche vectorielle).

Principe :
    1. La requête utilisateur est encodée en vecteur avec Sentence-Transformers
       (même modèle que celui utilisé lors de l'ETL, sinon les vecteurs ne sont
       pas comparables).
    2. Les vecteurs des programmes sont lus depuis SQLite (colonne BLOB).
    3. On calcule la similarité cosinus entre la requête et chaque programme.
    4. On retourne les top_k programmes les plus proches, avec un score en %.
"""

import json
import sqlite3
import time
from functools import lru_cache

import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from config import DB_PATH, EMBEDDING_MODEL_NAME

# Nom de la méthode enregistré dans recommendation_history.
# Il servira à distinguer l'Option A de l'Option B dans le dashboard de comparaison.
NOM_METHODE = "option_a_embeddings"


# ---------------------------------------------------------------------------
# Chargement du modèle
# ---------------------------------------------------------------------------

@lru_cache(maxsize=1)
def charger_modele():
    """
    Charge le modèle d'embedding une seule fois.

    Le chargement d'un SentenceTransformer prend plusieurs secondes : grâce au
    cache, les appels suivants réutilisent la même instance en mémoire.
    """
    return SentenceTransformer(EMBEDDING_MODEL_NAME)


# ---------------------------------------------------------------------------
# Étape 1 : encodage de la requête
# ---------------------------------------------------------------------------

def encoder_requete(requete_utilisateur):
    """
    Transforme la requête texte en vecteur float32 de forme (1, dimension).

    La forme 2D est celle attendue par sklearn.cosine_similarity.
    """
    modele = charger_modele()
    vecteur = modele.encode([requete_utilisateur])
    return np.asarray(vecteur, dtype=np.float32)


# ---------------------------------------------------------------------------
# Étapes 2 et 3 : lecture des programmes et conversion des BLOB
# ---------------------------------------------------------------------------

def charger_programmes():
    """
    Récupère les programmes et leurs embeddings depuis la base SQLite.

    Retourne :
        programmes (list[dict]) : informations descriptives de chaque programme
        matrice (np.ndarray)    : embeddings empilés, forme (nb_programmes, dimension)
    """
    connexion = sqlite3.connect(DB_PATH)
    try:
        curseur = connexion.cursor()
        # On ignore les programmes sans vecteur (ils ne peuvent pas être comparés)
        curseur.execute("""
            SELECT id, title, description, target_level, program_goal,
                   required_equipment, embedding_vector
            FROM workout_programs
            WHERE embedding_vector IS NOT NULL
        """)
        lignes = curseur.fetchall()
    finally:
        connexion.close()

    programmes = []
    vecteurs = []
    for (prog_id, titre, description, niveau, objectif, equipement, blob) in lignes:
        # Conversion des octets bruts en tableau numpy.
        # Le dtype doit être identique à celui utilisé à l'écriture (float32).
        vecteurs.append(np.frombuffer(blob, dtype=np.float32))
        programmes.append({
            "id": prog_id,
            "title": titre,
            "description": description,
            "target_level": niveau,
            "program_goal": objectif,
            "required_equipment": equipement,
        })

    if not vecteurs:
        return [], np.empty((0, 0), dtype=np.float32)

    # Empilement en une seule matrice pour un calcul vectorisé (bien plus rapide
    # qu'une boucle Python programme par programme)
    matrice = np.vstack(vecteurs)
    return programmes, matrice


# ---------------------------------------------------------------------------
# Historique : alimente le dashboard de comparaison A / B
# ---------------------------------------------------------------------------

def enregistrer_historique(user_id, requete_utilisateur, resultats, temps_ms):
    """
    Enregistre une recommandation dans la table recommendation_history.

    raw_output contient les résultats au format JSON (id, titre, score) afin
    de pouvoir les réafficher ou les analyser plus tard dans le dashboard.
    """
    sortie_brute = json.dumps(
        [
            {"id": r["id"], "title": r["title"], "score_similarite": r["score_similarite"]}
            for r in resultats
        ],
        ensure_ascii=False,
    )

    connexion = sqlite3.connect(DB_PATH)
    try:
        connexion.execute("""
            INSERT INTO recommendation_history
                (user_id, recommendation_method, user_query, raw_output, execution_time_ms)
            VALUES (?, ?, ?, ?, ?)
        """, (user_id, NOM_METHODE, requete_utilisateur, sortie_brute, temps_ms))
        connexion.commit()
    finally:
        connexion.close()


# ---------------------------------------------------------------------------
# Fonction principale : étapes 4 et 5
# ---------------------------------------------------------------------------

def recommander_option_a(requete_utilisateur, top_k=3, user_id=None, enregistrer=True):
    """
    Recommande les programmes les plus pertinents pour une requête utilisateur.

    Paramètres :
        requete_utilisateur (str) : besoin exprimé par l'utilisateur
                                    (ex : "programme débutant pour perdre du poids à la maison")
        top_k (int)               : nombre de programmes à retourner
        user_id (int | None)      : utilisateur à l'origine de la requête (facultatif)
        enregistrer (bool)        : si True, la recommandation est sauvegardée
                                    dans recommendation_history

    Retourne :
        list[dict] : les top_k programmes triés par pertinence décroissante,
                     chacun avec une clé "score_similarite" exprimée en %.
    """
    # Validation des entrées
    if not requete_utilisateur or not requete_utilisateur.strip():
        raise ValueError("La requête utilisateur ne peut pas être vide.")
    if top_k <= 0:
        raise ValueError("top_k doit être un entier strictement positif.")

    # Début du chronomètre (mesure du temps total de la recommandation)
    debut = time.perf_counter()

    # 1. Encodage de la requête
    vecteur_requete = encoder_requete(requete_utilisateur)

    # 2 & 3. Chargement des programmes et de leurs vecteurs
    programmes, matrice_programmes = charger_programmes()
    if not programmes:
        return []

    # Sécurité : la dimension doit correspondre (même modèle qu'à l'ETL)
    if vecteur_requete.shape[1] != matrice_programmes.shape[1]:
        raise ValueError(
            f"Dimension incompatible : requête {vecteur_requete.shape[1]} "
            f"vs base {matrice_programmes.shape[1]}. "
            "Vérifiez que EMBEDDING_MODEL_NAME est le même que lors de l'ETL."
        )

    # 4. Similarité cosinus : résultat de forme (1, nb_programmes) -> on prend la ligne 0
    scores = cosine_similarity(vecteur_requete, matrice_programmes)[0]

    # 5. Tri décroissant des scores et sélection des top_k indices
    top_k = min(top_k, len(programmes))
    indices_tries = np.argsort(scores)[::-1][:top_k]

    resultats = []
    for idx in indices_tries:
        programme = dict(programmes[idx])
        # Conversion du score cosinus en pourcentage (arrondi à 2 décimales)
        programme["score_similarite"] = round(float(scores[idx]) * 100, 2)
        resultats.append(programme)

    # Fin du chronomètre : temps en millisecondes (entier, comme dans le schéma)
    temps_ms = int((time.perf_counter() - debut) * 1000)

    if enregistrer:
        enregistrer_historique(user_id, requete_utilisateur, resultats, temps_ms)

    return resultats


# ---------------------------------------------------------------------------
# Test rapide en ligne de commande
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    requete = "Programme débutant pour prendre du muscle à la maison avec des haltères"
    print(f"🔎 Requête : {requete}\n")

    for rang, prog in enumerate(recommander_option_a(requete, top_k=3), start=1):
        print(f"{rang}. {prog['title']} — {prog['score_similarite']} %")
        print(f"   Objectif : {prog['program_goal']} | Niveau : {prog['target_level']}")
        print(f"   Équipement : {prog['required_equipment']}\n")
