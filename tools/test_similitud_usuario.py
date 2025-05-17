import os
from dotenv import load_dotenv
from pinecone import Pinecone
from langchain_openai import OpenAIEmbeddings

# Cargar variables de entorno
load_dotenv()

# Configuración
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-ada-002")
NAMESPACE = "tarjeta_cencopay"

# Inicializar servicios
pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(PINECONE_INDEX_NAME)
embedder = OpenAIEmbeddings(model=EMBEDDING_MODEL, openai_api_key=OPENAI_API_KEY)

# Script de test para probar similitud con las preguntas del usuario
def test_similitud_usuario():
    print(f"\n🧪 Test de similitud semántica en namespace: '{NAMESPACE}'\n")
    while True:
        entrada = input("❓ Ingresá una pregunta de prueba (o 'exit'): ").strip()
        if entrada.lower() == "exit":
            break

        try:
            vector = embedder.embed_query(entrada)
            res = index.query(
                vector=vector,
                top_k=3,
                include_metadata=True,
                namespace=NAMESPACE
            )

            print(f"\n📊 Matches encontrados: {len(res.matches)}")

            if not res.matches:
                print("❌ Ninguna pregunta similar relevante encontrada.")
                continue

            for match in res.matches:
                metadata = match.metadata
                score = match.score
                pregunta_faq = metadata.get("pregunta", "N/A")
                respuesta_sugerida = metadata.get("respuesta", "N/A")
                beneficios = metadata.get("beneficios_clave", [])
                tags = metadata.get("tags", [])
    
                print(f"\n--- Match con Score: {score:.4f} (ID: {match.id}) ---")
                print(f"🧠 Pregunta FAQ: {pregunta_faq}")
                print(f"💬 Respuesta Sugerida: {respuesta_sugerida}")
                if beneficios:
                    print(f"💡 Beneficios Clave: {', '.join(beneficios)}")
                if tags:
                    print(f"🏷️ Tags: {', '.join(tags)}")
                # Considera mostrar todos los top_k resultados para un mejor análisis durante el testeo
                # break 

        except Exception as e:
            print("❌ Error al buscar similitud:", e)

if __name__ == "__main__":
    test_similitud_usuario()