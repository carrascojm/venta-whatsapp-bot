import os
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAIEmbeddings
from openai import OpenAI
from supabase import create_client, Client
from faq_semantica import buscar_pregunta_similar
from memoria_avanzada import guardar_mensaje_en_pinecone_avanzado

load_dotenv()

# Configuraciones
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENV = os.getenv("PINECONE_ENVIRONMENT")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")
PINECONE_REGION = os.getenv("PINECONE_REGION")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-ada-002")

# Inicializar servicios
pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(PINECONE_INDEX_NAME)
embedding_model = OpenAIEmbeddings(model=EMBEDDING_MODEL, openai_api_key=OPENAI_API_KEY)
vector_store = PineconeVectorStore(index=index, embedding=embedding_model)
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# === FUNCIONES PRINCIPALES ===

def buscar_por_similitud(usuario_id):
    resultados = vector_store.similarity_search(usuario_id, k=3)
    return [r.page_content for r in resultados]

def guardar_en_historial(usuario_id, mensaje, tipo, producto):
    data = {"usuario_id": usuario_id, "mensaje": mensaje, "tipo": tipo, "producto": producto}
    try:
        supabase.table("interacciones").insert(data).execute()
    except Exception as e:
        print("❌ Error al guardar en Supabase:", e)

def construir_contexto_conversacional(usuario_id, max_turnos=5):
    try:
        response = supabase.table("interacciones") \
            .select("mensaje, tipo") \
            .eq("usuario_id", usuario_id) \
            .order("created_at", desc=False) \
            .limit(max_turnos * 2) \
            .execute()

        historial = []
        for row in response.data:
            if row["tipo"] == "usuario":
                historial.append(f"👤 Usuario: {row['mensaje']}")
            else:
                historial.append(f"🤖 Bot: {row['mensaje']}")
        return "\n".join(historial)
    except Exception as e:
        print("❌ Error al construir contexto:", e)
        return ""

def registrar_venta_simulada(usuario_id, producto, estado="interesado", decision_gpt=None):
    try:
        data = {
            "usuario_id": usuario_id,
            "producto": producto,
            "estado": estado,
            "decision_gpt": decision_gpt
        }
        supabase.table("ventas").insert(data).execute()
    except Exception as e:
        print("❌ Error al registrar venta:", e)

def detectar_intencion_compra(mensaje_usuario):
    try:
        client = OpenAI(api_key=OPENAI_API_KEY)
        system_prompt = (
            "Tu tarea es evaluar si el siguiente mensaje refleja una intención clara "
            "de compra o adquisición de un producto. Respondé solamente con 'sí' o 'no'."
        )
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": mensaje_usuario}
            ],
            temperature=0
        )
        decision_text = response.choices[0].message.content.strip().lower()
        return (decision_text == "sí", decision_text)
    except Exception as e:
        print("❌ Error en detección de intención de compra:", e)
        return (False, "error")

def obtener_producto_activo():
    try:
        response = supabase.table("productos").select("*").eq("activo", True).limit(1).execute()
        data = response.data
        if not data:
            return None
        return data[0]
    except Exception as e:
        print("❌ Error al obtener producto activo:", e)
        return None

def es_usuario_nuevo(usuario_id):
    try:
        response = supabase.table("interacciones").select("id").eq("usuario_id", usuario_id).limit(1).execute()
        return len(response.data) == 0
    except Exception as e:
        print("❌ Error verificando usuario:", e)
        return False

def generar_respuesta_persuasiva(usuario_id, mensaje_usuario, producto):
    # Guardar en Pinecone y Supabase
    guardar_mensaje_en_pinecone_avanzado(usuario_id, mensaje_usuario, producto=producto)
    guardar_en_historial(usuario_id, mensaje_usuario, tipo="usuario", producto=producto)

    # Preparar contexto
    historial = construir_contexto_conversacional(usuario_id)
    producto_info = obtener_producto_activo()
    if not producto_info:
        return "Actualmente no hay un producto activo para ofrecer."

    beneficios = "\n- " + "\n- ".join(producto_info["beneficios_secundarios"])
    objeciones = "\n- " + "\n- ".join(producto_info["posibles_objeciones"])
    
    namespace = producto.lower().replace(" ", "_")
    refuerzo_semantico = buscar_pregunta_similar(mensaje_usuario, namespace=namespace)
    
    refuerzo_txt = f"\n\nRespuesta sugerida: {refuerzo_semantico}" if refuerzo_semantico else ""

    # Armar prompt
    prompt = f"""
Sos un asistente persuasivo que está ayudando a vender el producto \"{producto_info['nombre']}\"
Beneficio principal: {producto_info['beneficio_principal']}

Otros beneficios:
{beneficios}

El usuario puede tener dudas como:
{objeciones}

Respondé con un estilo: {producto_info['estilo_comunicacion']}

Historial reciente del usuario:
{historial}

Nuevo mensaje del usuario:
{mensaje_usuario}
{refuerzo_txt}

Terminá tu respuesta con: {producto_info['llamado_a_la_accion']}
"""

    # Generar respuesta con GPT
    try:
        client = OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Estás vendiendo de forma persuasiva y empática."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        mensaje_bot = response.choices[0].message.content.strip()

        guardar_en_historial(usuario_id, mensaje_bot, tipo="bot", producto=producto)

        decision, decision_text = detectar_intencion_compra(mensaje_usuario)
        if decision:
            registrar_venta_simulada(
                usuario_id,
                producto=producto,
                estado="interesado",
                decision_gpt=decision_text
            )

        return mensaje_bot
    except Exception as e:
        print("❌ Error generando respuesta:", e)
        return "Hubo un error al procesar tu mensaje. Por favor intentá nuevamente."