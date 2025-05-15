import os
import hashlib
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def generar_id_deterministico(usuario_id, mensaje):
    texto = f"{usuario_id}_{mensaje.strip().lower()}"
    return hashlib.sha256(texto.encode()).hexdigest()

def guardar_en_historial(usuario_id, mensaje, tipo, producto, score_similitud=None, respuesta_final_ofrecida=None):
    id_deterministico = generar_id_deterministico(usuario_id, mensaje)

    data = {
        "id": id_deterministico,
        "usuario_id": usuario_id,
        "mensaje": mensaje,
        "tipo": tipo,
        "producto": producto
    }

    if score_similitud is not None:
        data["score_similitud"] = score_similitud

    if respuesta_final_ofrecida is not None:
        data["respuesta_final_ofrecida"] = respuesta_final_ofrecida

    try:
        supabase.table("interacciones").upsert(data).execute()
        print(f"✅ Registro guardado en Supabase con ID: {id_deterministico}")
    except Exception as e:
        print("❌ Error al guardar en Supabase:", e)
