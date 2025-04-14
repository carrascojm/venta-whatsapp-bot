# monitor.py

from core_bot import ver_historial_usuario, supabase
from langchain_pinecone import PineconeVectorStore

def ver_ventas_usuario(usuario_id):
    print(f"\n📋 VENTAS SIMULADAS DE {usuario_id.upper()}\n")
    try:
        response = supabase.table("ventas") \
            .select("producto, estado, decision_gpt, created_at") \
            .eq("usuario_id", usuario_id) \
            .order("created_at", desc=False) \
            .execute()

        if not response.data:
            print("🚫 No se encontraron ventas registradas para este usuario.")
            return

        for row in response.data:
            print(f"🛍️ Producto: {row['producto']}")
            print(f"📅 Fecha: {row['created_at']}")
            print(f"📌 Estado: {row['estado']}")
            print(f"🤖 Evaluación GPT: {row['decision_gpt']}")
            print("-" * 50)
    except Exception as e:
        print("❌ Error al consultar Supabase:", e)


def main():
    print("🧠 Herramienta de monitoreo del Bot de Ventas")
    print("1️⃣ Ver historial completo del usuario")
    print("2️⃣ Ver ventas simuladas del usuario")
    print("3️⃣ Salir")
    opcion = input("Seleccioná una opción: ").strip()

    if opcion not in ["1", "2"]:
        print("👋 ¡Hasta la próxima!")
        return

    # Entrada simplificada
    telefono = input("📲 Ingresá el número sin prefijo (ej: 5491158790474): ").strip()
    usuario_id = f"whatsapp:+{telefono}"

    if opcion == "1":
        ver_historial_usuario(usuario_id)
    elif opcion == "2":
        ver_ventas_usuario(usuario_id)

if __name__ == "__main__":
    main()