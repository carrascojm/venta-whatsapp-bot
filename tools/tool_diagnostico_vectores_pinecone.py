import os
from pinecone import Pinecone
from dotenv import load_dotenv

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")
NAMESPACE = "tarjeta_coto"

pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(PINECONE_INDEX_NAME)

def listar_vectores_con_metadata(namespace):
    try:
        print(f"🧾 Explorando namespace: {namespace}")

        # Buscar los primeros 100 vectores (ID conocidos o aleatorios)
        response = index.describe_index_stats()
        total_vectores = response.namespaces.get(namespace, {}).get("vector_count", 0)
        print(f"🔢 Total de vectores en {namespace}: {total_vectores}")

        # Vamos a intentar fetch de todos los vectores por ID usando el describe_index_stats (si soportado)
        # Alternativamente, harcodeamos 100 ids si tenemos una lógica para generarlos

        print("🔍 Intentando recuperar vectores...")
        ids_a_buscar = []  # completar si tenés forma de predecir los IDs o cargar un archivo
        if not ids_a_buscar:
            print("⚠️ No hay IDs para buscar. Este script necesita que le des un listado de IDs para inspeccionar.")
            return

        res = index.fetch(ids=ids_a_buscar, namespace=namespace)

        for vector_id, vector in res.vectors.items():
            metadata = vector.metadata
            if metadata.get("usuario_id", "").startswith("whatsapp:"):
                print(f"\n🧠 Vector ID: {vector_id}")
                print("📱 Usuario:", metadata.get("usuario_id"))
                print("💬 Mensaje:", metadata.get("mensaje"))
                print("🛍️ Producto:", metadata.get("producto"))
                print("🏷️ Tópicos:", metadata.get("topicos"))
    except Exception as e:
        print("❌ Error accediendo a Pinecone:", e)

if __name__ == "__main__":
    listar_vectores_con_metadata(NAMESPACE)