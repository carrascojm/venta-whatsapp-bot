import os
import hashlib
from dotenv import load_dotenv
from pinecone import Pinecone
from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAIEmbeddings
from openai import OpenAI
from postgrest.exceptions import APIError as PostgrestAPIError
from supabase import create_client, Client
from faq_semantica import buscar_pregunta_similar
from memoria_avanzada import guardar_mensaje_en_pinecone_avanzado
from utils import generar_id_deterministico

load_dotenv()

# Configuraciones
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-ada-002")

# Inicializar servicios
pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(PINECONE_INDEX_NAME)
embedding_model = OpenAIEmbeddings(model=EMBEDDING_MODEL, openai_api_key=OPENAI_API_KEY)
vector_store = PineconeVectorStore(index=index, embedding=embedding_model)
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# === FUNCIONES PRINCIPALES ===

def hash_mensaje(usuario_id, mensaje):
    return hashlib.md5((usuario_id + mensaje.lower().strip()).encode()).hexdigest()

def buscar_por_similitud(usuario_id):
    resultados = vector_store.similarity_search(usuario_id, k=3)
    return [r.page_content for r in resultados]

def guardar_en_historial(usuario_id, mensaje, tipo, producto, score_similitud=None, respuesta_final_ofrecida=None):
    interaccion_id = generar_id_deterministico(usuario_id, mensaje)

    data = {
        "id": interaccion_id,
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
        supabase.table("interacciones").insert(data).execute()
    except Exception as e:
        print("❌ Error al guardar en Supabase:", e)

def construir_contexto_conversacional(usuario_id, producto=None, max_turnos=5):
    """
    Recupera los últimos turnos de la conversación
    y devuelve solo el texto de cada mensaje, sin labels.
    """
    try:
        # Base query: filtrar por usuario y opcionalmente por producto
        query = supabase.table("interacciones") \
            .select("mensaje") \
            .eq("usuario_id", usuario_id)
        if producto:
            query = query.eq("producto", producto)

        # Traer los últimos max_turnos*2 mensajes en orden cronológico
        response = query \
            .order("created_at", desc=False) \
            .limit(max_turnos * 2) \
            .execute()

        # Extraer únicamente el texto de cada mensaje
        mensajes = [row["mensaje"] for row in response.data]
        return "\n".join(mensajes)

    except Exception as e:
        print("❌ Error al construir contexto:", e)
        return ""

def registrar_venta_simulada(usuario_id, producto, estado, decision_gpt):
    """
    Inserta o actualiza un registro de venta simulada en Supabase,
    manteniendo siempre el último estado ("interesado" o "no_interesado").
    """

    try:
        # Verificar si ya existe una venta para este usuario
        existing_response = supabase.table("ventas").select("id").eq("usuario_id", usuario_id).limit(1).execute()
        existing_data = existing_response.data

        if existing_data:
            # Si existe, hacer un UPDATE con el nuevo estado
            venta_id = existing_data[0]["id"]
            response = supabase.table("ventas").update({
                "producto": producto,
                "estado": estado,
                "decision_gpt": decision_gpt
            }).eq("id", venta_id).execute()

            if response.data: # supabase-py v2 devuelve los registros actualizados en .data
                print(f"♻️ Venta actualizada para {usuario_id}: {estado} ({decision_gpt})")
            else:
                # Éxito HTTP, pero no se devolvieron datos de la actualización.
                # Podría ser RLS, o que la fila no fue encontrada por ID (menos probable si existing_data fue encontrado).
                print(f"⚠️ Venta actualizada (o no encontrada/visible para actualizar), no se retornaron datos. Usuario: {usuario_id}. Estado HTTP OK. Datos: {response.data}")
        else:
            # Si no existe, hacer un INSERT
            # insert espera una lista de diccionarios
            response = supabase.table("ventas").insert([{
                "usuario_id": usuario_id,
                "producto": producto,
                "estado": estado,
                "decision_gpt": decision_gpt,
            }]).execute()

            if response.data: # supabase-py v2 devuelve los registros insertados en .data
                print(f"✅ Nueva venta registrada para {usuario_id}: {estado} ({decision_gpt})")
            else:
                # Éxito HTTP, pero no se devolvieron datos de la inserción.
                # Podría ser RLS u otras condiciones que no son errores.
                print(f"⚠️ Venta insertada, pero no se retornaron datos. Usuario: {usuario_id}. Estado HTTP OK. Datos: {response.data}")

    except PostgrestAPIError as e:
        print(f"❌ Error de PostgREST registrando venta simulada para {usuario_id}: {e.message} (Code: {getattr(e, 'code', 'N/A')}, Details: {getattr(e, 'details', 'N/A')})")
    except Exception as e:
        print(f"❌ Excepción general registrando venta simulada para {usuario_id}: {e}")

def check_si_ya_se_ofrecio_cierre(usuario_id, producto):
    try:
        response = supabase.table("interacciones") \
            .select("id") \
            .eq("usuario_id", usuario_id) \
            .eq("producto", producto) \
            .eq("respuesta_final_ofrecida", True) \
            .limit(1) \
            .execute()
        return len(response.data) > 0
    except Exception as e:
        print("❌ Error verificando si ya se ofreció cierre:", e)
        return False

def obtener_historial_usuario(usuario_id, producto):
    try:
        response = supabase.table("interacciones") \
            .select("mensaje, tipo") \
            .eq("usuario_id", usuario_id) \
            .eq("producto", producto) \
            .order("created_at", desc=False) \
            .execute()
        return response.data or []
    except Exception as e:
        print("❌ Error obteniendo historial completo:", e)
        return []

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

def detectar_tono_emocional(mensaje_usuario):
    try:
        client = OpenAI(api_key=OPENAI_API_KEY)
        system_prompt = (
            "Tu tarea es analizar el siguiente mensaje de un usuario y devolver en una sola palabra su tono emocional dominante. "
            "Usa palabras como: 'entusiasmado', 'dudoso', 'desconfiado', 'curioso', 'indiferente', 'emocionado', 'molesto', 'confundido'. "
            "Respondé SOLO con una de esas palabras o la más cercana. Nada más."
        )
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": mensaje_usuario}
            ],
            temperature=0
        )
        return response.choices[0].message.content.strip().lower()
    except Exception as e:
        print("❌ Error en detección de tono emocional:", e)
        return "neutro"

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
    # 0. Si el usuario responde “sí” tras un cierre ofrecido, vamos directo al cierre ———————
    afirmaciones = {"si","sí","dale","claro","me interesa","vamos","confirmo"}
    # Verifico si antes ya se ofreció el cierre
    if mensaje_usuario.strip().lower() in afirmaciones and check_si_ya_se_ofrecio_cierre(usuario_id, producto):
        respuesta_cierre = (
            "¡Genial! Para completar el alta necesito que me confirmes tu DNI, tu sexo y tu fecha de nacimiento."
        )
        # Registro en historial
        guardar_en_historial(usuario_id, mensaje_usuario, tipo="usuario", producto=producto)
        guardar_en_historial(usuario_id, respuesta_cierre, tipo="bot", producto=producto, respuesta_final_ofrecida=True)
        return respuesta_cierre
    
    # 1. Obtener producto activo y su system_prompt
    producto_info = obtener_producto_activo()
    if not producto_info:
        return "Actualmente no hay un producto activo para ofrecer."

    system_prompt = producto_info.get("prompt_system")
    if not system_prompt:
        return "No se encontró un prompt configurado para este producto."

    # 2. Obtener el último mensaje del usuario para la Regla de Objeciones
    historial_ultimo = supabase.table("interacciones") \
        .select("mensaje") \
        .eq("usuario_id", usuario_id) \
        .eq("producto", producto) \
        .order("created_at", desc=True) \
        .limit(1) \
        .execute().data
    ultimo_mensaje = historial_ultimo[0]["mensaje"] if historial_ultimo else mensaje_usuario

    bloque_objeciones = f"""
### REGLA DE OBJECIONES:
Última pregunta del cliente: "{ultimo_mensaje}"
Si detectás objeción, primero valida con una pregunta de clarificación y esperá su respuesta
antes de ofrecer beneficios.
"""

    # 3. Preparar historial de conversación
    historial = construir_contexto_conversacional(usuario_id)

    # 4. Buscar pregunta similar (FAQ) si existe
    refuerzo_semantico, score_similitud, origen_vector, beneficios_faq = buscar_pregunta_similar(mensaje_usuario, producto)
    mostrar_refuerzo = refuerzo_semantico and origen_vector == "faq"
    refuerzo_txt = (
        f"\n\nRespuesta sugerida basada en preguntas frecuentes: {refuerzo_semantico}"
        if mostrar_refuerzo else ""
    )

    beneficios_txt = ""
    if beneficios_faq:
        beneficios_str = ", ".join(beneficios_faq)
        beneficios_txt = (
            f"\n\nAl responder, considera resaltar sutilmente estos beneficios clave relacionados "
            f"con la consulta del usuario, si es pertinente: {beneficios_str}."
        )

    # 5. Preparar el prompt dinámico para el usuario, inyectando la Regla de Objeciones
    prompt_usuario = f"""{bloque_objeciones}

Historial reciente de la conversación:
{historial}

Considera la siguiente información al formular tu respuesta:
Mensaje del cliente:
{mensaje_usuario}
{refuerzo_txt}
Contexto adicional de la FAQ (si aplica): {beneficios_txt if mostrar_refuerzo else ""}
"""

    try:
        client = OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt_usuario}
            ],
            temperature=0.7
        )
        mensaje_bot = response.choices[0].message.content.strip()

        # 6. Guardar en Pinecone y Supabase
        guardar_mensaje_en_pinecone_avanzado(usuario_id, mensaje_usuario, producto=producto)
        guardar_en_historial(usuario_id, mensaje_usuario, tipo="usuario", producto=producto)
        guardar_en_historial(
            usuario_id,
            mensaje_bot,
            tipo="bot",
            producto=producto,
            score_similitud=score_similitud
        )

        # 7. Detectar intención de compra y registrar lead
        decision_compra, _ = detectar_intencion_compra(mensaje_usuario)
        estado_venta = "interesado" if decision_compra else "no_interesado"
        decision_texto = "sí" if decision_compra else "no"

        registrar_venta_simulada(
            usuario_id=usuario_id,
            producto=producto,
            estado=estado_venta,
            decision_gpt=decision_texto
        )

        return mensaje_bot

    except Exception as e:
        print("❌ Error generando respuesta:", e)
        return "Hubo un error al procesar tu mensaje. Por favor intentá nuevamente."
