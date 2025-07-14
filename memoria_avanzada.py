import os
import hashlib
from openai import OpenAI
from langchain_openai import OpenAIEmbeddings
from pinecone import Pinecone
from dotenv import load_dotenv
from utils import generar_id_deterministico

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-ada-002")

client = OpenAI(api_key=OPENAI_API_KEY)
embedder = OpenAIEmbeddings(model=EMBEDDING_MODEL, openai_api_key=OPENAI_API_KEY)
pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(PINECONE_INDEX_NAME)

def generar_id_vector_unico(usuario_id, mensaje):
    """
    Genera un ID único y determinístico combinando el número de usuario y un hash del mensaje.
    """
    hash_mensaje = hashlib.sha256(mensaje.encode("utf-8")).hexdigest()
    return f"{usuario_id}_{hash_mensaje}"

def extraer_topicos(mensaje):
    prompt = f"""
    Extraé los temas clave del siguiente mensaje en formato JSON como lista simple.
    Ejemplo de salida: ["descuentos", "seguridad"]

    Mensaje: "{mensaje}"
    """
    try:
        respuesta = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Sos un clasificador de temas de mensajes de clientes."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
        )
        texto = respuesta.choices[0].message.content.strip()
        topicos = eval(texto) if texto.startswith("[") else []
        return topicos
    except Exception as e:
        print("❌ Error extrayendo tópicos:", e)
        return []

def guardar_mensaje_en_pinecone_avanzado(usuario_id, mensaje, producto):
    try:
        topicos = extraer_topicos(mensaje)
        vector = embedder.embed_query(mensaje)

        vector_id = generar_id_deterministico(usuario_id, mensaje)

        metadata = {
            "usuario_id": usuario_id,
            "mensaje": mensaje,
            "producto": producto,
            "topicos": topicos,
            "tipo": "usuario",
            "origen": "upsert_directo"
        }

        print(f"\n🔢 Generando embedding...")
        print(f"📦 Haciendo upsert directo con ID: {vector_id}")

        index.upsert(
            vectors=[{
                "id": vector_id,
                "values": vector,
                "metadata": metadata
            }],
            namespace=producto.lower().replace(" ", "_")
        )

        print("\n✅ Vector guardado exitosamente en Pinecone.")
    except Exception as e:
        print("❌ Error al indexar mensaje en Pinecone:", e)
