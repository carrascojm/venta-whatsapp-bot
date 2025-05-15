import os
from dotenv import load_dotenv
from pinecone import Pinecone

# Cargar variables de entorno
load_dotenv()

# Configuración
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")
NAMESPACE = "tarjeta_cencopay"

# Inicializar Pinecone
pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(PINECONE_INDEX_NAME)

print(f"🧾 Listando TODOS los vectores en el namespace: {NAMESPACE}")

try:
    # Recolectar todos los IDs
    all_ids = []
    for page in index.list(namespace=NAMESPACE):
        if isinstance(page, list):
            all_ids.extend(page)
        else:
            all_ids.append(page)

    if not all_ids:
        print("❌ No hay vectores cargados en este namespace.")
    else:
        print(f"🔢 Total encontrados: {len(all_ids)}\n")

        for i, vec_id in enumerate(all_ids, 1):
            result = index.fetch(ids=[vec_id], namespace=NAMESPACE)
            vector_data = result.vectors.get(vec_id)
            metadata = vector_data.metadata if vector_data else {}

            print(f"--- Vector #{i} ---")
            print(f"📌 ID: {vec_id}")
            print(f"🧠 Mensaje: {metadata.get('mensaje', '(sin mensaje)')}")
            print(f"💬 Pregunta: {metadata.get('pregunta', '-')}")
            print(f"✅ Respuesta: {metadata.get('respuesta', '-')}")
            print(f"🔖 Producto: {metadata.get('producto', '-')}")
            print(f"🏷️  Tópicos: {metadata.get('topicos', '-')}")
            print(f"📦 Tipo: {metadata.get('tipo', '-')}")
            print(f"📍 Origen: {metadata.get('origen', '-')}")
            print()

except Exception as e:
    print(f"❌ Error al listar vectores: {e}")