# ver_historial.py

from core_bot import ver_historial_usuario

if __name__ == "__main__":
    print("🔎 Ver historial de usuario")
    usuario_id = input("📲 Ingresá el ID del usuario (ej: whatsapp:+54911...): ").strip()
    ver_historial_usuario(usuario_id)