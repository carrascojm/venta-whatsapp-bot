from pinecone import Pinecone
import os
from dotenv import load_dotenv

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")

pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(PINECONE_INDEX_NAME)

def mostrar_contenido(namespace="tarjeta_coto"):
    print(f"\n🧾 Listando contenido del namespace: {namespace}")
    try:
        stats = index.describe_index_stats()
        total = stats['namespaces'].get(namespace, {}).get('vector_count', 0)
        print(f"🔢 Total de vectores: {total}")

        if total == 0:
            print("⚠️ El namespace está vacío.")
            return

        # Extraer hasta 10 vectores mediante una query dummy
        dummy_vector = [0.0] * 1536
        results = index.query(
            vector=dummy_vector,
            top_k=10,
            namespace=namespace,
            include_metadata=True
        )

        if not results.matches:
            print("⚠️ No se encontraron vectores en la consulta.")
            return

        for i, match in enumerate(results.matches):
            metadata = match.metadata
            print(f"\n--- Vector #{i+1} ---")
            print(f"📌 ID: {match.id}")
            print(f"🧠 Pregunta: {metadata.get('pregunta')}")
            print(f"💬 Respuesta: {metadata.get('respuesta')}")

    except Exception as e:
        print("❌ Error accediendo a Pinecone:", e)

if __name__ == "__main__":
    mostrar_contenido()