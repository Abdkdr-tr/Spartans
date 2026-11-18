# Spartans
S5 BUT3 Info - équipe Les Blaireaux Intrépides
 
Projet de recommandation de programmes de fitness (backend Python + base SQLite avec embeddings).

## Lien du projet
https://github.com/Abdkdr-tr/Spartans

## Installation
 
### 1. Cloner le projet
 
```bash
git clone git@github.com:Abdkdr-tr/Spartans.git
cd Spartans
```
 
### 2. Créer et activer l'environnement virtuel
 
```bash
python3 -m venv .env
source .env/bin/activate
```
 
> Sous Windows : `.env\Scripts\activate`
 
### 3. Installer les dépendances
 
```bash
pip install -r requirements.txt
```
 
> Le `requirements.txt` utilise la version CPU de PyTorch via l'index
> `https://download.pytorch.org/whl/cpu`. L'installation peut prendre quelques minutes
> (environ 200 Mo pour `torch`).
 
## Base de données
 
Deux options : **télécharger la base déjà prête** (recommandé, rapide) ou **la générer** soi-même.
 
### Option A : télécharger le fichier `.db`
 
Le fichier `.db` (déjà rempli avec les programmes, exercices et embeddings) est disponible ici :
 
👉 **[Télécharger le fichier spartans.db](https://drive.google.com/file/d/1fAMl_iaALLUTQmtcAsagrZiZGAvYa2LV/view?usp=sharing)**
 
Une fois téléchargé, place-le dans `backend/app/database/` depuis la racine du projet.
Si le fichier est dans ton dossier Téléchargements :
 
```bash
mkdir -p backend/app/database
mv ~/Téléchargements/spartans.db backend/app/database/
```
 
> Si ton système est en anglais, le dossier s'appelle `~/Downloads`.
 
Vérifie que le fichier est bien en place :
 
```bash
ls backend/app/database/
```
 
### Option B : générer la base soi-même
 
Depuis la racine du projet, avec l'environnement virtuel activé :
 
```bash
cd backend/app/scriptdatabase
 
# 1. Créer les tables
python3 init_table_db.py
 
# 2. Télécharger le dataset Kaggle, calculer les embeddings et remplir la base
python3 init_data.py
```
 
Le script `init_data.py` :
 
- télécharge le dataset Kaggle *600k fitness exercise and workout program* ;
- nettoie les données avec Pandas ;
- calcule les embeddings avec le modèle `all-MiniLM-L6-v2` ;
- insère les programmes, les exercices et leurs liaisons dans SQLite.
Résultat attendu : environ **2 598 programmes**, **3 213 exercices** et **605 033 liaisons**
(compte environ 1 à 2 minutes).
 

