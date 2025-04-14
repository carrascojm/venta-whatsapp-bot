import uuid
import os
from dotenv import load_dotenv
from pinecone import Pinecone
from langchain_openai import OpenAIEmbeddings

load_dotenv()

# Config
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-ada-002")
NAMESPACE = "tarjeta_coto"

# Init Pinecone
pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(PINECONE_INDEX_NAME)

# Init embeddings
embedder = OpenAIEmbeddings(model=EMBEDDING_MODEL, openai_api_key=OPENAI_API_KEY)

# Mensaje
usuario_id = "whatsapp:+5491150000000"
mensaje = "Este es un mensaje indexado directamente con upsert."
producto = "Tarjeta Coto"
vector_id = f"{usuario_id}_{uuid.uuid4()}"

# Obtener embedding
print("🔢 Generando embedding...")
embedding = embedder.embed_query(mensaje)

# Guardar vector manualmente
print(f"📦 Haciendo upsert directo con ID: {vector_id}")
index.upsert(
    vectors=[{
        "id": vector_id,
        "values": embedding,
        "metadata": {
            "usuario_id": usuario_id,
            "mensaje": mensaje,
            "producto": producto,
            "tipo": "usuario",
            "origen": "upsert_directo"
        }
    }],
    namespace=NAMESPACE
)

# Verificar
print("\n🔍 Verificando guardado...")
res = index.fetch(ids=[vector_id], namespace=NAMESPACE)
vector = res.vectors.get(vector_id)

if vector:
    print(f"\n✅ Vector encontrado con ID: {vector_id}")
    print("📌 Metadata guardada:")
    for k, v in vector.metadata.items():
        print(f"   - {k}: {v}")
else:
    print("❌ No se encontró el vector. Algo falló.")