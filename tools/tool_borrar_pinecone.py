# borrar_pinecone.py

from pinecone import Pinecone
import os
from dotenv import load_dotenv

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")

pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(PINECONE_INDEX_NAME)

# ⚠️ CUIDADO: borra todo
index.delete(delete_all=True)

print("🧼 Todos los vectores fueron eliminados de Pinecone.")