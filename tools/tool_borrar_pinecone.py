import os
from dotenv import load_dotenv
from pinecone import Pinecone
from langchain_openai import OpenAIEmbeddings

load_dotenv()

# Configuración
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-ada-002")

# Inicialización
pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(PINECONE_INDEX_NAME)
namespace = "tarjeta_cencopay"

try:
    index.delete(delete_all=True, namespace=namespace)
    print(f"🧹 Namespace '{namespace}' eliminado correctamente.")
except Exception as e:
    print(f"❌ Error al eliminar namespace: {e}")