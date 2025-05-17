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
    stats = index.describe_index_stats()
    namespace_stats = stats.namespaces.get(NAMESPACE)

    if not namespace_stats or namespace_stats.vector_count == 0:
        print("❌ No hay vectores cargados en este namespace.")
    else:
        total_vectores = namespace_stats.vector_count
        print(f"🔢 Total de vectores en el namespace: {total_vectores}\n")

        # Listar todos los IDs (puede ser una lista grande)
        # Pinecone-client v3.x.x: index.list_ids() es un generador
        ids_in_namespace = list(index.list_ids(namespace=NAMESPACE))
        
        if not ids_in_namespace:
            print("❌ No se encontraron IDs de vectores, aunque las estadísticas indican que existen.")
        else:
            print(f"🔍 Obtenidos {len(ids_in_namespace)} IDs. Realizando fetch en batches de 100...")
            
            fetched_count = 0
            for i in range(0, len(ids_in_namespace), 100):
                batch_ids = ids_in_namespace[i:i+100]
                if not batch_ids:
                    continue
                
                results = index.fetch(ids=batch_ids, namespace=NAMESPACE)
                for vec_id, vector_data in results.vectors.items():
                    fetched_count +=1
                    metadata = vector_data.metadata if vector_data else {}

                    print(f"--- Vector #{fetched_count} (Total procesados: {i + list(results.vectors.keys()).index(vec_id) + 1}) ---")
                    print(f"📌 ID: {vec_id}")
                    # Mostrar metadatos relevantes
                    for key, value in metadata.items():
                        print(f"  {key.capitalize()}: {value}")
                    print()
            print(f"✅ Listado completo. Total de vectores mostrados: {fetched_count}")

except Exception as e:
    print(f"❌ Error al listar vectores: {e}")