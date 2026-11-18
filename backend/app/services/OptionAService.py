import json
import time

import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from app.services.WorkoutProgramService import WorkoutProgramService
from app.services.RecommendationHistoryService import RecommendationHistoryService
from app.scriptdatabase.config import DB_PATH,EMBEDDING_MODEL_NAME


NOM_METHODE = "option_a_embeddings"



class OptionAService:

   
   def __init__(self):
       self.model = SentenceTransformer(EMBEDDING_MODEL_NAME)
       self.wps  = WorkoutProgramService()
       self.rhs  = RecommendationHistoryService()


   def _encoder_requete(self, requete_utilisateur):
       vecteur = self.model.encode([requete_utilisateur])
       return np.asarray(vecteur,dtype=np.float32)

   def _charger_programmes(self):
       embedding_vectors_pairs = self.wps.findAllEmbeddingVectors()
       programmes = []
       vecteurs = []
       for program_id,blob in embedding_vectors_pairs:
           vecteurs.append(np.frombuffer(blob,dtype=np.float32))
           programmes.append(self.wps.findByIdWithoutEmbeddingVector(program_id))
       
       if not vecteurs:
          return [], np.empty((0,0),dtype=np.float32)
       
       matrice = np.vstack(vecteurs)
       return programmes,matrice

   def _enregistrer_historique(self, user_id, requete_utilisateur, resultats, temps_ms):
      
      sortie_brute = json.dumps(
         [
           {"id":r["id"],"title":["title"], "score_similarite":r["score_similarite"]}
           for r in resultats
         ],
         ensure_ascii=False,
      )
      history_data = {user_id,NOM_METHODE,requete_utilisateur,sortie_brute,temps_ms}
      self.rhs.add(history_data)
   
  
   def recommendation_option_a(self, requete_utilisateur, top_k=3, user_id=None, enregistrer=True):
       
       if not requete_utilisateur or not requete_utilisateur.strip():
          raise ValueError("La requête utilisateur ne peut pas être vide")
       if top_k <= 0:
          raise ValueError("top_k doit être un entier strictement positif")

       debut = time.perf_counter()

       vecteur_requete = self._encoder_requete(requete_utilisateur)

       programmes,matrice_prog = self._charger_programmes()
       if not programmes:
            return []
        
       if vecteur_requete.shape[1] != matrice_prog.shape[1]:
          raise ValueError("Mauvaise dimensions")

       score = cosine_similarity(vecteur_requete,matrice_prog)[0]

       top_k = min(top_k,len(programmes))
       indices_tries = np.argsort(score)[::-1][:top_k]

       resultats = []
       for idx in indices_tries:
           programme = dict(programmes[idx])
           programme["score_similarite"] = round(float(score[idx]) * 100,2)
           resultats.append(programme)       

       temps_ms = int((time.perf_counter() - debut) * 1000)
   
       if enregistrer:  
          self._enregistrer_historique(user_id,requete_utilisateur,resultats,temps_ms)
      
       return resultats