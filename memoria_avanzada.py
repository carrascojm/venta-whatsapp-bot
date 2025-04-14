import uuid
import os
from openai import OpenAI
from langchain_openai import OpenAIEmbeddings
from pinecone import Pinecone
from langchain_pinecone import PineconeVectorStore
from dotenv import load_dotenv

load_dotenv()

# Configuración
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENV = os.getenv("PINECONE_ENVIRONMENT")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-ada-002")

# Inicialización
client = OpenAI(api_key=OPENAI_API_KEY)
embedding_model = OpenAIEmbeddings(model=EMBEDDING_MODEL, openai_api_key=OPENAI_API_KEY)
pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(PINECONE_INDEX_NAME)
vector_store = PineconeVectorStore(index=index, embedding=embedding_model)

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
    topicos = extraer_topicos(mensaje)
    metadata = {
        "usuario_id": usuario_id,
        "mensaje": mensaje,
        "producto": producto,
        "topicos": topicos,
        "origen": "usuario"
    }
    try:
        vector_store.add_texts(
        texts=[mensaje],
        ids=[f"{usuario_id}_{uuid.uuid4()}"],
        metadatas=[metadata],
        namespace=producto.lower().replace(" ", "_")  # ej: Tarjeta Coto -> tarjeta_coto
    )
        print(f"✅ Mensaje indexado con tópicos y producto: {producto} | Tópicos: {topicos}")
    except Exception as e:
        print("❌ Error indexando mensaje con metadatos:", e)