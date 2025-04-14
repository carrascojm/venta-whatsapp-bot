import os
from dotenv import load_dotenv
from pinecone import Pinecone
from langchain_openai import OpenAIEmbeddings

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")
PINECONE_REGION = os.getenv("PINECONE_REGION")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-ada-002")

pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(PINECONE_INDEX_NAME)

def buscar_pregunta_similar(mensaje_usuario, namespace="tarjeta_coto", umbral_similitud=0.35):
    """
    Dada una pregunta del usuario, busca en Pinecone si hay alguna FAQ similar.
    Si encuentra una con similitud suficiente, devuelve la respuesta sugerida.
    """
    try:
        embedder = OpenAIEmbeddings(model=EMBEDDING_MODEL, openai_api_key=OPENAI_API_KEY)
        vector = embedder.embed_query(mensaje_usuario)

        res = index.query(
            vector=vector,
            top_k=1,
            include_metadata=True,
            namespace=namespace
        )

        if res.matches and res.matches[0].score >= umbral_similitud:
            mejor_respuesta = res.matches[0].metadata.get("respuesta", None)
            if mejor_respuesta:
                print(f"\n🤔 Pregunta similar encontrada (score {res.matches[0].score:.2f}):")
                print("Pregunta:", res.matches[0].metadata.get("pregunta"))
                print("Respuesta sugerida:", mejor_respuesta)
                return mejor_respuesta
        else:
            print("\n❌ Ninguna pregunta similar relevante encontrada.")
            return None

    except Exception as e:
        print("\n❌ Error buscando pregunta similar:", e)
        return None

# Prueba directa
if __name__ == "__main__":
    mensaje = input("👀 Ingresá una pregunta para buscar en Pinecone: ").strip()
    respuesta = buscar_pregunta_similar(mensaje)
    if respuesta:
        print("\n💡 Respuesta sugerida:", respuesta)
    else:
        print("\n(Sin sugerencia relevante)")