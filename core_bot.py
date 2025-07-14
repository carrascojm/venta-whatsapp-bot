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
    try:
        query = supabase.table("interacciones").select("mensaje").eq("usuario_id", usuario_id)
        if producto:
            query = query.eq("producto", producto)
        response = query.order("created_at", desc=False).limit(max_turnos*2).execute()
        mensajes = [row["mensaje"] for row in response.data]
        return "\n".join(mensajes)
    except Exception as e:
        print("❌ Error al construir contexto:", e)
        return ""


def registrar_venta_simulada(usuario_id, producto, estado, decision_gpt):
    try:
        existing = supabase.table("ventas").select("id").eq("usuario_id", usuario_id).limit(1).execute().data
        if existing:
            venta_id = existing[0]["id"]
            resp = supabase.table("ventas").update({
                "producto": producto,
                "estado": estado,
                "decision_gpt": decision_gpt
            }).eq("id", venta_id).execute()
            if resp.data:
                print(f"♻️ Venta actualizada para {usuario_id}: {estado} ({decision_gpt})")
        else:
            resp = supabase.table("ventas").insert([{"usuario_id": usuario_id, "producto": producto, "estado": estado, "decision_gpt": decision_gpt}]).execute()
            if resp.data:
                print(f"✅ Nueva venta registrada para {usuario_id}: {estado} ({decision_gpt})")
    except PostgrestAPIError as e:
        print(f"❌ Error PostgREST en ventas para {usuario_id}: {e.message}")
    except Exception as e:
        print(f"❌ Excepción general registrando venta para {usuario_id}: {e}")


def detectar_intencion_compra(mensaje_usuario):
    try:
        client = OpenAI(api_key=OPENAI_API_KEY)
        prompt = (
            "Tu tarea es evaluar si el siguiente mensaje refleja una intención clara "
            "de compra o adquisición de un producto. Respondé solamente con 'sí' o 'no'."
        )
        resp = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role":"system","content":prompt},{"role":"user","content":mensaje_usuario}],
            temperature=0
        )
        txt = resp.choices[0].message.content.strip().lower()
        return (txt == "sí", txt)
    except Exception as e:
        print("❌ Error en intención de compra:", e)
        return (False, "error")


def detectar_tono_emocional(mensaje_usuario):
    try:
        client = OpenAI(api_key=OPENAI_API_KEY)
        prompt = (
            "Tu tarea es analizar el siguiente mensaje y devolver en una sola palabra "
            "su tono emocional dominante (ej.: 'entusiasmado','dudoso','confundido')."
        )
        resp = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role":"system","content":prompt},{"role":"user","content":mensaje_usuario}],
            temperature=0
        )
        return resp.choices[0].message.content.strip().lower()
    except Exception:
        return "neutro"


def obtener_producto_activo():
    try:
        data = supabase.table("productos").select("*").eq("activo", True).limit(1).execute().data
        return data[0] if data else None
    except Exception as e:
        print("❌ Error al obtener producto activo:", e)
        return None


def es_usuario_nuevo(usuario_id):
    try:
        resp = supabase.table("interacciones").select("id").eq("usuario_id", usuario_id).limit(1).execute().data
        return len(resp) == 0
    except Exception as e:
        print("❌ Error verificando usuario:", e)
        return False


def generar_respuesta_persuasiva(usuario_id, mensaje_usuario, producto):
    # 0. Cierre tras confirmación explícita
    afirmaciones = {"si","sí","dale","claro","me interesa","vamos","confirmo"}
    last_bot = supabase.table("interacciones").select("mensaje,respuesta_final_ofrecida").eq("usuario_id",usuario_id).eq("producto",producto).eq("tipo","bot").order("created_at",desc=True).limit(1).execute().data
    if last_bot and (mensaje_usuario.strip().lower() in afirmaciones and last_bot[0].get("respuesta_final_ofrecida")):
        respuesta = "¡Genial! Para completar el alta necesito que me confirmes tu DNI, tu sexo y tu fecha de nacimiento."
        guardar_en_historial(usuario_id, mensaje_usuario, "usuario", producto)
        guardar_en_historial(usuario_id, respuesta, "bot", producto, respuesta_final_ofrecida=True)
        return respuesta

    # 1. Off-topic semántico: leer flag
    last_off = supabase.table("interacciones").select("id,off_topic").eq("usuario_id",usuario_id).eq("producto",producto).eq("tipo","bot").order("created_at",desc=True).limit(1).execute().data
    off_flag = bool(last_off and last_off[0].get("off_topic"))
    off_id = last_off[0]["id"] if last_off else None

    # 2. Configuración y prompt_system
    prod_info = obtener_producto_activo()
    if not prod_info: return "Actualmente no hay un producto activo para ofrecer."
    system_prompt = prod_info.get("prompt_system") or ""

    # 3. Similaridad semántica
    refuerzo, score, origen, beneficios = buscar_pregunta_similar(mensaje_usuario, producto)
    TH = 0.2
    if score < TH and origen != "faq" and not off_flag:
        resp_off = "Entiendo tu consulta, pero solo puedo ayudarte con tarjetas Cencopay. Si querés saber de beneficios, límites o costos, preguntame con confianza."
        guardar_en_historial(usuario_id, mensaje_usuario, "usuario", producto)
        guardar_en_historial(usuario_id, resp_off, "bot", producto)
        if off_id:
            supabase.table("interacciones").update({"off_topic":True}).eq("id",off_id).execute()
        return resp_off
    if off_flag and score >= TH and origen == "faq":
        if off_id:
            supabase.table("interacciones").update({"off_topic":False}).eq("id",off_id).execute()

    # 4. Regla de objeciones
    hist_ult = supabase.table("interacciones").select("mensaje").eq("usuario_id",usuario_id).eq("producto",producto).order("created_at",desc=True).limit(1).execute().data
    ult = hist_ult[0]["mensaje"] if hist_ult else mensaje_usuario
    rule = f"""### REGLA DE OBJECIONES:\nÚltima pregunta: '{ult}'\nValida antes de ofrecer beneficios.\n"""

    # 5. Crear prompt de usuario
    hist = construir_contexto_conversacional(usuario_id)
    ref_txt = f"\n\nRespuesta FAQ: {refuerzo}" if (refuerzo and origen=="faq") else ""
    ben_txt = f"\n\nResaltar beneficios: {', '.join(beneficios)}." if beneficios else ""
    user_prompt = f"{rule}\nHistorial:\n{hist}\nUsuario:{mensaje_usuario}{ref_txt}{ben_txt}"

    try:
        client = OpenAI(api_key=OPENAI_API_KEY)
        res = client.chat.completions.create(model="gpt-4", messages=[{"role":"system","content":system_prompt},{"role":"user","content":user_prompt}], temperature=0.7)
        bot_msg = res.choices[0].message.content.strip()
        guardar_mensaje_en_pinecone_avanzado(usuario_id, mensaje_usuario, producto=producto)
        guardar_en_historial(usuario_id, mensaje_usuario, "usuario", producto, score_similitud=score)
        guardar_en_historial(usuario_id, bot_msg, "bot", producto, score_similitud=score)
        dec_comp, _ = detectar_intencion_compra(mensaje_usuario)
        estado = "interesado" if dec_comp else "no_interesado"
        registrar_venta_simulada(usuario_id, producto, estado, "sí" if dec_comp else "no")
        return bot_msg
    except Exception as e:
        print("❌ Error generando respuesta:", e)
        return "Hubo un error al procesar tu mensaje. Por favor intentá nuevamente."