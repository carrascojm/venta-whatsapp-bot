import os
from dotenv import load_dotenv
from supabase import create_client, Client
from pinecone import Pinecone

load_dotenv()

# Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Pinecone
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")
pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(PINECONE_INDEX_NAME)


def mostrar_estado_supabase():
    print("\n=== INTERACCIONES EN SUPABASE ===")
    try:
        res = supabase.table("interacciones").select("*").order("created_at", desc=True).limit(10).execute()
        for r in res.data:
            print(f"[{r['tipo'].upper()}] {r['usuario_id']}: {r['mensaje']}")
    except Exception as e:
        print("❌ Error leyendo Supabase:", e)


def mostrar_estado_pinecone(usuario_id):
    print("\n=== HISTORIAL VECTORIAL EN PINECONE ===")
    try:
        res = index.fetch(ids=[usuario_id])
        if not res.vectors:
            print("(Sin datos para este usuario)")
            return

        for id_, vec in res.vectors.items():
            metadata = vec.get("metadata", {})
            print(f"ID: {id_}")
            print(f"Contenido: {metadata.get('text', '[sin texto]')}")
    except Exception as e:
        print("❌ Error leyendo Pinecone:", e)


if __name__ == "__main__":
    usuario = input("🔎 Ingresá el número de celular (sin whatsapp:): ").strip()
    if not usuario.startswith("whatsapp:"):
        usuario = f"whatsapp:{usuario}"

    mostrar_estado_supabase()
    mostrar_estado_pinecone(usuario)
