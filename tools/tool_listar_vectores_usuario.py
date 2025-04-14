import os
from dotenv import load_dotenv
from pinecone import Pinecone

# Cargar variables de entorno
load_dotenv()

# Configuración
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")
NAMESPACE = "tarjeta_coto"

# Inicializar Pinecone
pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(PINECONE_INDEX_NAME)

print(f"🧾 Listando vectores generados por usuarios en namespace: {NAMESPACE}")

try:
    # Aseguramos que all_ids sea una lista plana de strings
    flat_ids = []
    for page in index.list(namespace=NAMESPACE):
        if isinstance(page, list):
            flat_ids.extend(page)
        else:
            flat_ids.append(page)

    # Filtramos solo los que comienzan con whatsapp:
    user_vectors = [vec_id for vec_id in flat_ids if isinstance(vec_id, str) and vec_id.startswith("whatsapp:")]

    if not user_vectors:
        print("🔎 No se encontraron vectores generados por usuarios.")
    else:
        print(f"🔢 Total encontrados: {len(user_vectors)}\n")

        for i, vec_id in enumerate(user_vectors, 1):
            result = index.fetch(ids=[vec_id], namespace=NAMESPACE)
            vector_data = result.vectors.get(vec_id)
            metadata = vector_data.metadata if vector_data else {}

            print(f"--- Vector #{i} ---")
            print(f"📌 ID: {vec_id}")
            print(f"🧠 Mensaje: {metadata.get('mensaje', '(sin mensaje)')}")
            print(f"🔖 Producto: {metadata.get('producto', '-')}")
            print(f"🏷️  Tópicos: {metadata.get('topicos', '-')}")
            print()

except Exception as e:
    print(f"❌ Error al listar vectores: {e}")