import hashlib

def hash_mensaje(texto):
    return hashlib.sha256(texto.strip().lower().encode()).hexdigest()


def generar_id_vector_unico(usuario_id, mensaje):
    """
    Devuelve un ID único basado en el usuario y el contenido del mensaje,
    así evitamos duplicados exactos en Pinecone.
    """
    hash_msj = hash_mensaje(mensaje)
    return f"{usuario_id}_{hash_msj}"


def ya_existe_en_supabase(supabase, usuario_id, mensaje, producto):
    """
    Verifica si ya existe un mensaje idéntico en Supabase para ese usuario y producto.
    """
    try:
        response = supabase.table("interacciones") \
            .select("id") \
            .eq("usuario_id", usuario_id) \
            .eq("mensaje", mensaje.strip()) \
            .eq("producto", producto) \
            .limit(1) \
            .execute()

        return len(response.data) > 0
    except Exception as e:
        print("❌ Error verificando duplicado en Supabase:", e)
        return False


def ya_existe_en_pinecone(index, vector_id, namespace):
    try:
        resultado = index.fetch(ids=[vector_id], namespace=namespace)
        return vector_id in resultado.vectors
    except Exception as e:
        print("❌ Error verificando duplicado en Pinecone:", e)
        return False
