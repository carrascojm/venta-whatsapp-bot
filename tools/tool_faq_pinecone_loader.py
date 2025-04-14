import os
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
from langchain_openai import OpenAIEmbeddings

load_dotenv()

# Configs
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")
PINECONE_REGION = os.getenv("PINECONE_REGION")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-ada-002")

# Inicializar Pinecone y OpenAI
pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(PINECONE_INDEX_NAME)
embedder = OpenAIEmbeddings(model=EMBEDDING_MODEL, openai_api_key=OPENAI_API_KEY)

# FAQ por producto
faq_tarjeta_coto = [
    {
        "pregunta": "¿La tarjeta tiene algún costo de mantenimiento?",
        "respuesta": "No, la Tarjeta Coto no tiene ningún costo de emisión ni de mantenimiento.",
    },
    {
        "pregunta": "¿Qué beneficios tengo con la tarjeta?",
        "respuesta": "Con la Tarjeta Coto obtenés un 5% de descuento en todas tus compras y hasta un 20% en productos seleccionados.",
    },
    {
        "pregunta": "¿Cómo se solicita la tarjeta?",
        "respuesta": "La podés solicitar completando un formulario online y la recibís en tu domicilio sin costo.",
    },
    {
        "pregunta": "¿Sirve para cualquier sucursal?",
        "respuesta": "Sí, la Tarjeta Coto se puede usar en cualquier sucursal del país y en compras online.",
    },
    {
        "pregunta": "¿Y si no la uso mucho?",
        "respuesta": "Incluso con poco uso, podés aprovechar grandes ahorros con cada compra y promociones exclusivas."
    }
]

# Cargar a Pinecone
namespace = "tarjeta_coto"
print(f"\n✨ Cargando preguntas frecuentes en el namespace: {namespace}")

for i, item in enumerate(faq_tarjeta_coto):
    texto = item["pregunta"]
    vector = embedder.embed_query(texto)
    index.upsert(vectors=[{
        "id": f"faq_{i}",
        "values": vector,
        "metadata": {
            "pregunta": item["pregunta"],
            "respuesta": item["respuesta"]
        }
    }], namespace=namespace)

print("✅ Preguntas cargadas exitosamente.")
