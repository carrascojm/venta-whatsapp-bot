# tools/loader_faq_tarjeta_cencopay_extendido.py
import os
from dotenv import load_dotenv
from pinecone import Pinecone
from langchain_openai import OpenAIEmbeddings

load_dotenv()

# Configs
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-ada-002")
NAMESPACE = "tarjeta_cencopay"

# Inicializar Pinecone y OpenAI
pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(PINECONE_INDEX_NAME)
embedder = OpenAIEmbeddings(model=EMBEDDING_MODEL, openai_api_key=OPENAI_API_KEY)

# Nuevas FAQs 
faq_tarjeta_cencopay = [
    {
        "pregunta": "¿Qué es la Tarjeta de Crédito CencoPay?",
        "respuesta": "Es una tarjeta de crédito emitida por Cencosud que te permite realizar compras en comercios adheridos y acceder a beneficios exclusivos, como descuentos y promociones especiales."
    },
    {
        "pregunta": "¿Dónde puedo usar la Tarjeta CencoPay?",
        "respuesta": "Podés utilizarla en los comercios adheridos a CencoPay, tanto de forma presencial como online. Esto incluye tiendas como Jumbo, Santa Isabel, Paris, Easy y SPID."
    },
    {
        "pregunta": "¿Cuáles son los beneficios de usar la Tarjeta CencoPay?",
        "respuesta": "Al usar tu Tarjeta CencoPay, accedés a promociones exclusivas, descuentos en compras, posibilidad de pagar en cuotas sin interés y acumulás puntos Cencosud para canjear por productos y servicios."
    },
    {
        "pregunta": "¿Cómo solicito la Tarjeta CencoPay?",
        "respuesta": "Podés solicitarla a través de la aplicación CencoPay o en el sitio web oficial. Deberás completar un formulario con tus datos personales y seguir los pasos indicados para la aprobación."
    },
    {
        "pregunta": "¿Tiene algún costo la Tarjeta CencoPay?",
        "respuesta": "La emisión de la tarjeta es gratuita. Sin embargo, pueden aplicarse cargos por mantenimiento o administración, según las condiciones vigentes. Te recomendamos consultar los términos y condiciones actualizados en el sitio oficial."
    },
    {
        "pregunta": "¿Cómo consulto el saldo y movimientos de mi Tarjeta CencoPay?",
        "respuesta": "Podés consultar tu saldo y movimientos ingresando a la aplicación CencoPay o al sitio web oficial con tu usuario y contraseña. Allí encontrarás toda la información detallada de tus consumos y pagos."
    },
    {
        "pregunta": "¿Qué hago si pierdo mi Tarjeta CencoPay?",
        "respuesta": "En caso de pérdida o robo, debés comunicarte inmediatamente con el centro de atención al cliente de CencoPay para bloquear la tarjeta y solicitar una nueva. También podés realizar esta gestión desde la aplicación."
    },
    {
        "pregunta": "¿Puedo pagar en cuotas con la Tarjeta CencoPay?",
        "respuesta": "Sí, la Tarjeta CencoPay te permite financiar tus compras en cuotas, según las promociones vigentes y las condiciones de cada comercio adherido."
    },
    {
        "pregunta": "¿Cómo accedo a las promociones exclusivas de CencoPay?",
        "respuesta": "Las promociones están disponibles en la sección de ofertas de la aplicación CencoPay y en el sitio web oficial. Te recomendamos revisarlas periódicamente para aprovechar los beneficios."
    },
    {
        "pregunta": "¿Qué debo hacer para dar de baja mi Tarjeta CencoPay?",
        "respuesta": "Para solicitar la baja de tu tarjeta, debés comunicarte con el servicio de atención al cliente de CencoPay, donde te guiarán en el proceso y te informarán sobre los pasos a seguir."
    }
]

# Cargar en Pinecone
print(f"\n✨ Cargando nuevas preguntas frecuentes en namespace: {NAMESPACE}")

for i, item in enumerate(faq_tarjeta_cencopay):
    texto = item["pregunta"]
    vector = embedder.embed_query(texto)
    index.upsert(vectors=[{
        "id": f"faq_extra_{i}",
        "values": vector,
        "metadata": {
            "pregunta": item["pregunta"],
            "respuesta": item["respuesta"]
        }
    }], namespace=NAMESPACE)

print("✅ Preguntas extendidas cargadas exitosamente.")