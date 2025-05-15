import os
import time
from dotenv import load_dotenv
from pinecone import Pinecone
from supabase import create_client
from core_bot import generar_respuesta_persuasiva

load_dotenv()

# === Config ===
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
NAMESPACE = "tarjeta_cencopay"

# === Inicializaciones ===
pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(PINECONE_INDEX_NAME)
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# === Utilidades ===
def borrar_todo():
    print("\n🧹 Borrando vectores de Pinecone...")
    try:
        index.delete(delete_all=True, namespace=NAMESPACE)
        print("✅ Vectores borrados del namespace.")
    except Exception as e:
        print("❌ Error borrando Pinecone:", e)

    print("\n🧹 Borrando interacciones y ventas en Supabase...")
    try:
        supabase.table("interacciones").delete().neq("id", "0").execute()
        supabase.table("ventas").delete().not_.is_("id", None).execute()
        print("✅ Interacciones y ventas borradas.")
    except Exception as e:
        print("❌ Error en Supabase:", e)

    input("\n🛑 Verificá en Supabase y Pinecone que todo esté limpio. Presioná ENTER para continuar...")

    print("\n📥 Cargando nuevamente las FAQ del producto activo en Pinecone...")
    os.system("python tools/tool_faq_pinecone_loader.py")
    print("✅ FAQ cargadas exitosamente.")

def simular_dialogo(usuario_id, producto, mensajes):
    for mensaje in mensajes:
        print(f"\n📩 {usuario_id} dice: {mensaje}")
        respuesta = generar_respuesta_persuasiva(usuario_id, mensaje, producto)
        print(f"🤖 Bot responde: {respuesta[:200]}...\n")
        time.sleep(0.5)

def mostrar_datos_guardados():
    print("\n📊 Interacciones registradas:")
    interacciones = supabase.table("interacciones").select("*").order("created_at").execute().data
    for i in interacciones:
        print(f"[{i['tipo']}] {i['usuario_id']}: {i['mensaje']} | score={i.get('score_similitud', '-')}, cierre={i.get('respuesta_final_ofrecida', '-')}")

    print("\n🧾 Ventas simuladas:")
    ventas = supabase.table("ventas").select("*").execute().data
    for v in ventas:
        print(f"{v['usuario_id']} → {v['estado']} ({v['decision_gpt']})")

# === Casos de prueba emocionales ===
cliente_emocional_1 = "whatsapp:+5491130000001"
mensajes_1 = [
    "Holaaa!! Estoy re entusiasmado, me contaron que la tarjeta tiene banda de beneficios 😍",
    "¿Posta que me descuentan en todas las compras?",
    "¡Dale! Contame cómo se pide porque la quiero ya!!"
]

cliente_emocional_2 = "whatsapp:+5491130000002"
mensajes_2 = [
    "No sé si confiar, estas tarjetas siempre tienen letra chica...",
    "Seguro hay algún costo escondido, ¿no?",
    "Convenceme de que vale la pena, porque no quiero otra tarjeta al pedo."
]

cliente_emocional_3 = "whatsapp:+5491130000003"
mensajes_3 = [
    "Che, no entiendo nada. ¿Cómo se usa esta tarjeta?",
    "¿Sirve para cualquier compra o solo algunas?",
    "¿Y si no la uso seguido? ¿Pierdo beneficios?"
]

cliente_emocional_4 = "whatsapp:+5491130000004"
mensajes_4 = [
    "¡Quiero sacar la tarjeta ya! ¿Cómo hago?",
    "Sí, sí, la quiero usar para aprovechar descuentos.",
    "¡Dale, avancemos!"
]

# === Script principal ===
if __name__ == "__main__":
    borrar_todo()

    producto = "Tarjeta Cencopay"

    simular_dialogo(cliente_emocional_1, producto, mensajes_1)
    simular_dialogo(cliente_emocional_2, producto, mensajes_4)

    mostrar_datos_guardados()