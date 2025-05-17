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
            "respuesta": "Es una tarjeta de crédito emitida por Cencosud que te permite realizar compras en comercios adheridos y acceder a beneficios exclusivos, como descuentos y promociones especiales.",
            "tags": ["definicion_producto", "general", "beneficios_multiples"],
            "keywords": ["tarjeta de crédito", "cencosud", "beneficios", "descuentos", "promociones"],
            "beneficios_clave": ["Acceso a descuentos exclusivos", "Promociones especiales en compras", "Facilidad de pago"]
    },
    {
        "pregunta": "¿Dónde puedo usar la Tarjeta CencoPay?",
            "respuesta": "Podés utilizarla en los comercios adheridos a CencoPay, tanto de forma presencial como online. Esto incluye tiendas como Jumbo, Santa Isabel, Paris, Easy y SPID.",
            "tags": ["uso_tarjeta", "comercios_adheridos", "versatilidad"],
            "keywords": ["jumbo", "santa isabel", "paris", "easy", "spid", "online", "presencial"],
            "beneficios_clave": ["Amplia red de comercios", "Comodidad para compras online y físicas", "Variedad de rubros (supermercado, hogar, etc.)"]
    },
    {
        "pregunta": "¿Cuáles son los beneficios de usar la Tarjeta CencoPay?",
            "respuesta": "Al usar tu Tarjeta CencoPay, accedés a promociones exclusivas, descuentos en compras, posibilidad de pagar en cuotas sin interés y acumulás puntos Cencosud para canjear por productos y servicios. ¡Es una herramienta genial para que tu dinero rinda más y disfrutes de recompensas!",
            "tags": ["beneficios_principales", "ahorro", "recompensas", "financiacion"],
            "keywords": ["promociones", "descuentos", "cuotas sin interes", "puntos cencosud", "ahorrar dinero"],
            "beneficios_clave": ["Ahorro significativo en compras", "Flexibilidad de pago con cuotas", "Recompensas por tus consumos (puntos)", "Acceso a ofertas únicas"]
    },
    {
        "pregunta": "¿Cómo solicito la Tarjeta CencoPay?",
            "respuesta": "¡Solicitarla es muy fácil! Podés hacerlo directamente desde la aplicación CencoPay o en nuestro sitio web oficial. Solo completás un formulario con tus datos y seguís unos simples pasos. ¡Podrías estar disfrutando de sus beneficios muy pronto!",
            "tags": ["proceso_solicitud", "facilidad", "online", "app"],
            "keywords": ["pedir tarjeta", "como obtener", "requisitos", "aplicacion"],
            "beneficios_clave": ["Proceso de solicitud rápido y sencillo", "Accesible desde app o web", "Mínimos requisitos"]
    },
    {
        "pregunta": "¿Tiene algún costo la Tarjeta CencoPay?",
            "respuesta": "La emisión de tu Tarjeta CencoPay es ¡totalmente gratuita! Pueden existir cargos de mantenimiento, pero suelen ser muy competitivos y se compensan con creces con todos los ahorros y beneficios que obtenés. Siempre podés consultar los términos actualizados en nuestro sitio.",
            "tags": ["costos_tarjeta", "mantenimiento", "transparencia"],
            "keywords": ["precio", "comisiones", "tarifa", "gratis"],
            "beneficios_clave": ["Emisión sin costo", "Cargos de mantenimiento razonables y compensados por beneficios"]
    },
    {
        "pregunta": "¿Cómo consulto el saldo y movimientos de mi Tarjeta CencoPay?",
            "respuesta": "Tenés control total de tu tarjeta. Podés consultar tu saldo y todos tus movimientos de forma fácil y rápida ingresando a la aplicación CencoPay o a nuestro sitio web con tu usuario.",
            "tags": ["gestion_cuenta", "consulta_saldo", "movimientos", "control_gastos"],
            "keywords": ["ver gastos", "extracto", "resumen de cuenta", "app cencopay"],
            "beneficios_clave": ["Fácil acceso a información financiera", "Control total sobre tus gastos", "Disponibilidad 24/7 desde app o web"]
    },
    {
        "pregunta": "¿Qué hago si pierdo mi Tarjeta CencoPay?",
            "respuesta": "¡No te preocupes! En caso de pérdida o robo, comunicate inmediatamente con nuestro centro de atención al cliente o, más rápido aún, bloqueala desde la app CencoPay para tu seguridad y solicitá una nueva.",
            "tags": ["seguridad_tarjeta", "perdida_robo", "bloqueo_tarjeta"],
            "keywords": ["tarjeta perdida", "extravio", "denuncia", "seguridad"],
            "beneficios_clave": ["Protección inmediata en caso de pérdida/robo", "Gestión rápida de bloqueo y reposición"]
    },
    {
        "pregunta": "¿Puedo pagar en cuotas con la Tarjeta CencoPay?",
            "respuesta": "¡Por supuesto! Una de las grandes ventajas es que podés financiar tus compras en cuotas, aprovechando las promociones vigentes. Ideal para esas compras más grandes o para organizar mejor tus pagos.",
            "tags": ["financiacion", "pago_cuotas", "flexibilidad_pago"],
            "keywords": ["pagar en partes", "financiar", "meses sin interes", "compras grandes"],
            "beneficios_clave": ["Flexibilidad para financiar compras", "Posibilidad de acceder a productos de mayor valor", "Mejor organización financiera"]
    },
    {
        "pregunta": "¿Cómo accedo a las promociones exclusivas de CencoPay?",
            "respuesta": "Es muy fácil estar al tanto de todas las promos. Las encontrás actualizadas en la sección de ofertas de la app CencoPay y en nuestro sitio web. ¡Te recomiendo chequearlas seguido para no perderte nada!",
            "tags": ["promociones_exclusivas", "ofertas", "ahorro_adicional"],
            "keywords": ["beneficios exclusivos", "oportunidades", "descuentos especiales"],
            "beneficios_clave": ["Acceso continuo a nuevas ofertas", "Maximización del ahorro", "Beneficios adicionales por ser cliente"]
    },
    {
        "pregunta": "¿Qué debo hacer para dar de baja mi Tarjeta CencoPay?",
            "respuesta": "Si en algún momento decidís que ya no la necesitás, el proceso de baja es simple. Solo tenés que comunicarte con nuestro servicio de atención al cliente y ellos te guiarán paso a paso.",
            "tags": ["proceso_baja", "cancelacion_tarjeta", "atencion_cliente"],
            "keywords": ["cancelar tarjeta", "dar de baja servicio", "terminar contrato"],
            "beneficios_clave": ["Proceso de baja claro y asistido"]
    }
]

# Cargar en Pinecone
print(f"\n✨ Cargando nuevas preguntas frecuentes en namespace: {NAMESPACE}")
vectors_to_upsert = []
for i, item in enumerate(faq_tarjeta_cencopay):
    # Embeddear una combinación de pregunta y respuesta puede dar mejor contexto
    texto_a_embeddear = f"Pregunta del usuario: {item['pregunta']} Respuesta relevante: {item['respuesta']}"
    vector = embedder.embed_query(texto_a_embeddear)
    
    metadata = {
        "pregunta": item["pregunta"],
        "respuesta": item["respuesta"],
        "origen": "faq_cencopay_v2", # Para identificar la fuente de estos datos
        "tipo_info": "faq" # Podrías tener otros tipos como "beneficio_detalle", "objecion_respuesta"
    }
    if "tags" in item:
        metadata["tags"] = item["tags"]
    if "keywords" in item:
        metadata["keywords"] = item["keywords"]
    if "beneficios_clave" in item:
        metadata["beneficios_clave"] = item["beneficios_clave"]

    vectors_to_upsert.append({
        "id": f"faq_cencopay_{NAMESPACE}_{i}", # ID más descriptivo
        "values": vector,
        "metadata": metadata
    })

    # Upsert en batches para mejor rendimiento con Pinecone
    if len(vectors_to_upsert) >= 50 or i == len(faq_tarjeta_cencopay) - 1:
        if vectors_to_upsert:
            index.upsert(vectors=vectors_to_upsert, namespace=NAMESPACE)
            print(f"Cargados {len(vectors_to_upsert)} vectores en batch.")
            vectors_to_upsert = []
    
print("✅ Preguntas extendidas cargadas exitosamente.")