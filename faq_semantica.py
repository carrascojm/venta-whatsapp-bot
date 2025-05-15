import os
from dotenv import load_dotenv
from pinecone import Pinecone
from langchain_openai import OpenAIEmbeddings

load_dotenv()

# Configuración
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-ada-002")

# Inicializar servicios
pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(PINECONE_INDEX_NAME)
embedder = OpenAIEmbeddings(model=EMBEDDING_MODEL, openai_api_key=OPENAI_API_KEY)

# ===============================
# FUNCIÓN PRINCIPAL DE MATCHING
# ===============================
def buscar_pregunta_similar(pregunta_usuario, producto, umbral=0.7):
    namespace = producto.lower().replace(" ", "_")
    try:
        vector = embedder.embed_query(pregunta_usuario)
        resultados = index.query(
            vector=vector,
            top_k=5,
            include_metadata=True,
            namespace=namespace
        )

        print(f"\n📊 Matches encontrados: {len(resultados.matches)}")

        for match in resultados.matches:
            metadata = match.metadata
            score = match.score

            print(f"📋 Metadata crudo recibido:\n{metadata}")
            print(f"📊 Score obtenido: {score:.4f}")

            if metadata and "respuesta" in metadata and score >= umbral:
                print("✅ Pregunta similar encontrada:")
                print(f"🧠 Pregunta FAQ: {metadata.get('pregunta')}")
                print(f"💬 Respuesta sugerida: {metadata.get('respuesta')}")
                return metadata["respuesta"], score, "faq"

        print("❌ Ninguna pregunta similar relevante encontrada.")
        return None, None, None

    except Exception as e:
        print("❌ Error en la búsqueda semántica:", e)
        return None, None, None