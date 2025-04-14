# tool_listar_vectores_usuario.py

import os
from dotenv import load_dotenv
from pinecone import Pinecone

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")
NAMESPACE = "tarjeta_coto"

pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(PINECONE_INDEX_NAME)

print(f"🧾 Listando vectores generados por usuarios en namespace: {NAMESPACE}")

try:
    vector_ids = index.list(namespace=NAMESPACE)

    # Filtrar los que no empiecen con "faq_"
    user_ids = [vid for vid in vector_ids if isinstance(vid, str) and not vid.startswith("faq_")]

    if not user_ids:
        print("🔎 No se encontraron vectores generados por usuarios.")
    else:
        print(f"🔢 Total de vectores generados por usuarios encontrados: {len(user_ids)}")
        for i, vid in enumerate(user_ids, 1):
            print(f"{i}. ID: {vid}")

except Exception as e:
    print(f"❌ Error al listar vectores: {e}")