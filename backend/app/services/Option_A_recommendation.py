import json
from functools import lru_cache

import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from app.services.WorkoutProgramService import WorkoutProgramService
from app.services.RecommendationHistoryService import RecommendationHistoryService
from app.scriptdatabase.config import DB_PATH,EMBEDDING_MODEL_NAME


NOM_METHODE = "option_a_embeddings"



class Option_A_RecommendationService:

   
   def __init__(self):
       self.model = SentenceTransformer(EMBEDDING_MODEL_NAME)
       self.wps  = WorkoutProgramService()
       self.rhs  = RecommendationHistoryService()


   def encoder_requete(requete_utilisateur):
       vecteur = self.model.encode([requete_utilisateur])
       return np.asarray(vecteur,dtype=np.float32)

   def charger_programmes():
       embedding_vectors_pairs = wps.findAllEmbeddingVectors()
       programes = []
       vecteurs = []
       for program_id,blob in embedding_vectors_pairs:
           vecteurs.append(np.frombuffer(blob,dtype=np.float32))
           programes.append(wps.)







