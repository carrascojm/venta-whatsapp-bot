import os
from supabase import create_client, Client


def fetch_interactions(whatsapp_number: str, max_records: int = 100):
    """
    Recupera interacciones de Supabase para un número de WhatsApp dado.

    Args:
        whatsapp_number (str): Número en formato 'whatsapp:+54911...' que identifica al usuario.
        max_records (int): Número máximo de interacciones a recuperar (default: 100).

    Returns:
        List[dict]: Lista de registros de interacciones.
    """
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    if not url or not key:
        raise EnvironmentError(
            "Define SUPABASE_URL y SUPABASE_KEY como variables de entorno."
        )

    supabase: Client = create_client(url, key)
    # Ejecutar consulta
    response = (
        supabase
        .table("interacciones")
        .select("usuario_id, mensaje, tipo, producto, created_at")
        .eq("usuario_id", whatsapp_number)
        .order("created_at", desc=False)
        .limit(max_records)
        .execute()
    )

    # Obtener datos directamente; supabase-py v2 lanza excepción si hay error
    registros = response.data if hasattr(response, 'data') else []
    return registros


if __name__ == "__main__":
    import json

    # Solicitar parámetros al usuario
    numero = 'whatsapp:' + input("Ingrese el número de WhatsApp (ejemplo '+5491131804612'): ").strip()
    max_str = input("Ingrese la cantidad máxima de registros a recuperar [default 100]: ").strip()
    try:
        max_records = int(max_str) if max_str else 100
    except ValueError:
        print("Valor inválido para máximo; usando 100.")
        max_records = 100

    # Ejecutar la consulta
    try:
        registros = fetch_interactions(numero, max_records)
        print(json.dumps(registros, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"Error: {e}")