# ver_ventas.py

from core_bot import supabase

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


if __name__ == "__main__":
    print("🔎 Ver ventas simuladas por usuario")
    usuario_id = input("📲 Ingresá el ID del usuario (ej: whatsapp:+54911...): ").strip()
    ver_ventas_usuario(usuario_id)