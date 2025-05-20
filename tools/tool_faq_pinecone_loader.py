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
        "pregunta": "¿Cómo genero un usuario para ingresar?",
        "respuesta": "Una vez que te bajaste la APP CENCOPAY o ingresaste en la web www.cencopay.com.ar, regístrate siguiendo los pasos, vas a necesitar tener a mano tu DNI físico ya que este va a ser tu usuario.",
        "tags": ["crear_usuario", "registro", "acceso"],
        "keywords": ["usuario", "ingresar", "registro", "app cencopay", "web cencopay", "DNI"],
        "beneficios_clave": ["Proceso de registro sencillo", "Acceso desde app o web"]
    },
    {
        "pregunta": "¿Quiénes son los responsables frente al BCRA? ¿Cuáles son los datos de contacto?",
        "respuesta": "Los funcionarios de Cencosud son los responsables. La titular es Elizabeth Varela, Jefe de Customer Service, Retail Financiero, y la suplente es Silvia Carletti, Supervisora Back Office Sugerencias y Reclamos, Retail Financiero. Puedes contactarlos al teléfono (011) 4733-1000 Int: 60748, de Lunes a Viernes de 9 a 16 hs, en Paraná 3617, Edificio 200, CP: 1640, Martinez, o al correo electrónico atencionserviciosfinancieros@cencosud.com.ar.",
        "tags": ["contacto", "BCRA", "reclamos", "responsables"],
        "keywords": ["contacto", "BCRA", "Cencosud", "Elizabeth Varela", "Silvia Carletti", "atención al cliente"],
        "beneficios_clave": ["Información de contacto clara", "Canales de comunicación disponibles"]
    },
    {
        "pregunta": "¿Qué necesito para poder operar con mi cuenta?",
        "respuesta": "Tenés que tener el nivel máximo de seguridad en tu cuenta. Esto lo lográs ingresando desde la app a la opción 'Ajustes' > 'Seguridad'. Allí podrás ver el nivel de seguridad y conocer las operaciones permitidas.",
        "tags": ["seguridad_cuenta", "operaciones", "configuracion_app"],
        "keywords": ["seguridad", "cuenta", "app", "ajustes", "nivel de seguridad"],
        "beneficios_clave": ["Mayor seguridad en las operaciones", "Control sobre las operaciones permitidas"]
    },
    {
        "pregunta": "¿Qué pasa si olvido mi contraseña?",
        "respuesta": "Si olvidás tu contraseña, podés recuperarla haciendo click en '¿Olvidaste tu contraseña?' dentro de la instancia de login.",
        "tags": ["contraseña", "recuperacion", "seguridad"],
        "keywords": ["olvidé contraseña", "recuperar acceso", "login"],
        "beneficios_clave": ["Proceso de recuperación de contraseña sencillo"]
    },
    {
        "pregunta": "Quiero cambiar mi contraseña",
        "respuesta": "En la Web: Andá a Inicio, deslizá hasta la sección 'Mi Cuenta' e ingresá a la opción 'Cambio de contraseña'. En la App: Andá a 'Ajustes' > 'Seguridad' > 'Cambiar contraseña'.",
        "tags": ["cambiar_contraseña", "seguridad", "gestion_cuenta"],
        "keywords": ["cambiar contraseña", "seguridad", "web", "app"],
        "beneficios_clave": ["Fácil gestión de la contraseña", "Control de seguridad personal"]
    },
    {
        "pregunta": "¿Bloqueaste tu usuario?",
        "respuesta": "Por cuestiones de seguridad, al cumplirse el tercer intento de acceso fallido se bloqueará automáticamente el usuario. Para desbloquearlo tenés que ir a la opción 'Olvidé mi contraseña' y seguir los pasos.",
        "tags": ["bloqueo_usuario", "seguridad", "acceso_cuenta"],
        "keywords": ["usuario bloqueado", "desbloquear", "seguridad", "login fallido"],
        "beneficios_clave": ["Protección automática de la cuenta", "Proceso de desbloqueo guiado"]
    },
    {
        "pregunta": "¿Por qué algunas veces solicitan validar mis datos?",
        "respuesta": "Para cuidar tu seguridad, te solicitaremos validar tu identidad al realizar transacciones.",
        "tags": ["seguridad", "validacion_datos", "transacciones"],
        "keywords": ["validar identidad", "seguridad transacciones", "protección"],
        "beneficios_clave": ["Mayor seguridad en las transacciones", "Protección de la identidad"]
    },
    {
        "pregunta": "¿Dónde realizo el cambio de domicilio?",
        "respuesta": "Lo puedes realizar a través de nuestro centro de atención al cliente al 0810-9999-627 de Lunes a Viernes de 9 a 19 hs.",
        "tags": ["cambio_datos", "domicilio", "atencion_cliente"],
        "keywords": ["cambiar domicilio", "actualizar datos", "teléfono de contacto"],
        "beneficios_clave": ["Facilidad para actualizar datos personales"]
    },
    {
        "pregunta": "Quiero cambiar mi número de teléfono",
        "respuesta": "En la Web: Desde el Menú principal, deslizá hasta la sección 'Mi Cuenta' e ingresá a 'Datos personales'. Allí podrás modificar tu número de celular. Recordá escribir el código de área sin cero y el número sin el quince. En la App: Desde el inicio, buscá 'Ajustes' en el menú principal, ingresá a 'Datos personales' y modificá tu celular. Recordá escribir el código de área sin cero y el número sin el quince.",
        "tags": ["cambio_datos", "telefono", "gestion_cuenta"],
        "keywords": ["cambiar teléfono", "actualizar contacto", "web", "app", "datos personales"],
        "beneficios_clave": ["Proceso de cambio de teléfono sencillo", "Flexibilidad para actualizar información"]
    },
    {
        "pregunta": "Quiero cambiar mi email",
        "respuesta": "En la Web: Desde el Menú principal, deslizá hasta la sección 'Mi Cuenta' e ingresá a 'Datos personales'. Allí podrás ver tu email actual y modificarlo. En la App: Desde el inicio, buscá 'Ajustes' en el menú principal, ingresá a 'Datos personales' y modificá tu email. La dirección de correo es muy importante ya que es donde te contactaremos.",
        "tags": ["cambio_datos", "email", "gestion_cuenta"],
        "keywords": ["cambiar email", "actualizar correo", "web", "app", "datos personales"],
        "beneficios_clave": ["Facilidad para actualizar email", "Asegura comunicación efectiva"]
    },
    {
        "pregunta": "No puedo recibir el código de validación porque cambié mi celular/email",
        "respuesta": "Podés cambiar tu información de contacto muy fácil. En la Web: Desde el Menú principal, deslizá hasta la sección 'Mi Cuenta' e ingresá a 'Datos personales'. En la App: Desde el inicio, buscá 'Ajustes' en el menú principal e ingresá a 'Datos personales'. Allí podrás ver tu información actual y elegir entre cambiar tu e-mail o celular.",
        "tags": ["codigo_validacion", "cambio_datos", "problemas_acceso"],
        "keywords": ["código de validación", "no recibo código", "cambiar celular", "cambiar email"],
        "beneficios_clave": ["Solución rápida para problemas de validación", "Flexibilidad para actualizar información de contacto"]
    },
    {
        "pregunta": "Me robaron el celular donde tenía la app de Cencopay",
        "respuesta": "Deberás ingresar a tu cuenta desde otro dispositivo, cambiar la contraseña desde 'Olvidé mi contraseña' y generar la denuncia desde la opción 'Denunciar tarjeta'.",
        "tags": ["robo_celular", "seguridad", "denuncia_tarjeta"],
        "keywords": ["celular robado", "app cencopay", "seguridad cuenta", "denunciar tarjeta"],
        "beneficios_clave": ["Protección inmediata de la cuenta", "Proceso de denuncia y cambio de contraseña facilitado"]
    },
    {
        "pregunta": "Quiero cerrar sesión",
        "respuesta": "Desde la Web: Presioná el botón 'Salir' que se encuentra en la parte superior del Inicio. Desde la App: Buscá la opción 'Ajustes' en el menú principal e ingresá a la opción 'Cerrar sesión'.",
        "tags": ["cerrar_sesion", "seguridad", "gestion_cuenta"],
        "keywords": ["cerrar sesión", "salir", "desloguear", "web", "app"],
        "beneficios_clave": ["Control de seguridad personal", "Facilidad para cerrar sesión"]
    },
    {
        "pregunta": "¿Cómo sé si soy persona políticamente expuesta o sujeto obligado?",
        "respuesta": "Se refiere a Funcionarios Públicos Nacionales, Provinciales y Municipales (tanto Nacionales como Extranjeros) de los Poderes Ejecutivo, Legislativo y Judicial, que ocupan o que ocuparon altos cargos puestos jerárquicos, así como a sus familiares hasta el segundo grado de consanguinidad.",
        "tags": ["definicion_legal", "PPE", "sujeto_obligado"],
        "keywords": ["persona políticamente expuesta", "sujeto obligado", "funcionarios públicos", "BCRA"],
        "beneficios_clave": ["Claridad en la definición de términos legales"]
    },
    {
        "pregunta": "¿Qué es la UIF?",
        "respuesta": "La Unidad de Información Financiera (UIF) se encarga del análisis, tratamiento y transmisión de información para prevenir e impedir el lavado de activos provenientes de delitos como tenencia y comercialización ilícita de estupefacientes, contrabando de armas, actividades de una asociación ilícita o terrorista, fraudes, delitos contra la Administración Pública, prostitución de menores, pornografía infantil y financiación del terrorismo.",
        "tags": ["definicion_legal", "UIF", "prevencion_delito"],
        "keywords": ["UIF", "lavado de activos", "delitos financieros", "prevención"],
        "beneficios_clave": ["Información sobre la función de la UIF"]
    },
    {
        "pregunta": "¿Por qué me piden una declaración jurada?",
        "respuesta": "La UIF tiene la facultad de solicitar informes, documentos, antecedentes y todo otro elemento útil para el cumplimiento de sus funciones a organismos públicos y a personas humanas o jurídicas, quienes están obligados a proporcionarlos bajo apercibimiento de ley.",
        "tags": ["declaracion_jurada", "requisitos_legales", "UIF"],
        "keywords": ["declaración jurada", "requisitos legales", "UIF", "cumplimiento normativo"],
        "beneficios_clave": ["Transparencia en los requisitos solicitados"]
    },
    {
        "pregunta": "¿Cómo proceder en caso de fallecimiento del titular?",
        "respuesta": "En caso de fallecimiento del titular, los familiares o adicionales deben solicitar la baja de la cuenta presentando el certificado de defunción. Si los adicionales realizaron consumos con fecha posterior al fallecimiento, deberán abonarlos primero para poder proceder con la baja.",
        "tags": ["fallecimiento_titular", "baja_cuenta", "documentacion"],
        "keywords": ["fallecimiento", "baja de cuenta", "certificado de defunción", "consumos pendientes"],
        "beneficios_clave": ["Proceso claro para la baja por fallecimiento"]
    },
    {
        "pregunta": "¿Qué son los datos biométricos? ¿Por qué me los piden?",
        "respuesta": "Los datos biométricos son información personal única de un individuo, como huellas dactilares, voz y rostro, utilizados para identificación precisa mediante sistemas tecnológicos. Los datos biométricos faciales son comunes en seguridad, como reconocimiento facial. Se solicitan como una medida adicional de seguridad para garantizar que solo el propietario de la cuenta tenga acceso, evitando el uso no autorizado.",
        "tags": ["seguridad", "datos_biometricos", "autenticacion"],
        "keywords": ["biométricos", "huellas dactilares", "reconocimiento facial", "seguridad cuenta", "verificación identidad"],
        "beneficios_clave": ["Mayor seguridad de la cuenta", "Protección contra uso no autorizado"]
    },
    {
        "pregunta": "¿Dónde puedo ver mi resumen de cuenta?",
        "respuesta": "Si realizaste consumos o tenés saldos pendientes, lo recibirás en tu casilla de correo y podrás descargarlo a través de nuestra Web o APP. En la App: Seleccioná la tarjeta, hacé click sobre el producto. En la Web: Seleccioná el botón 'Ver más', deslizá hasta 'Descarga tu Resumen'.",
        "tags": ["resumen_cuenta", "consulta_saldo", "gestion_cuenta"],
        "keywords": ["resumen", "estado de cuenta", "descargar resumen", "app", "web", "saldo"],
        "beneficios_clave": ["Acceso fácil y rápido al resumen", "Control de gastos disponible en todo momento"]
    },
    {
        "pregunta": "¿Cómo sé qué nivel de seguridad tengo?",
        "respuesta": "Esta información la obtenés únicamente dentro de la Aplicación. En la app, en la parte de 'Ajustes' debés seleccionar la opción 'Seguridad', la cual muestra el nivel actual sobre ese dispositivo y las operaciones permitidas, donde también podrás aumentarlo.",
        "tags": ["seguridad_cuenta", "nivel_seguridad", "app"],
        "keywords": ["nivel de seguridad", "app", "ajustes", "seguridad dispositivo"],
        "beneficios_clave": ["Control sobre el nivel de seguridad de la cuenta", "Facilidad para aumentar la seguridad"]
    },
    {
        "pregunta": "¿Qué conceptos aparecen detallados en el resumen de cuenta?",
        "respuesta": "En el resumen de cuenta podrás encontrar: Detalles de débitos automáticos, fechas de operaciones, detalle de la operación (nombre del comercio), importe de las transacciones en pesos/dólares, número de cuota debitada sobre el total del plan (ej. 1/3), y pagos en pesos y dólares ya realizados.",
        "tags": ["resumen_cuenta", "detalle_consumos", "informacion_financiera"],
        "keywords": ["conceptos resumen", "débitos automáticos", "operaciones", "cuotas", "pagos"],
        "beneficios_clave": ["Transparencia en la información del resumen", "Detalle completo de transacciones"]
    },
    {
        "pregunta": "¿Cómo puedo saber las cuotas pendientes que tengo?",
        "respuesta": "Desde la App: Seleccioná la tarjeta, presioná sobre el producto y después 'Ver todo', buscá la opción 'Cuotas pendientes'. Desde la Web: Seleccioná la tarjeta, presioná 'Ver más', deslizá hasta 'Consultas' y buscá 'Cuotas pendientes'.",
        "tags": ["cuotas_pendientes", "financiacion", "gestion_cuenta"],
        "keywords": ["cuotas", "pagos pendientes", "financiación", "app", "web"],
        "beneficios_clave": ["Fácil consulta de cuotas pendientes", "Control sobre la financiación"]
    },
    {
        "pregunta": "Tengo consumos que no reconozco",
        "respuesta": "Contactate con nosotros al 0810-9999-627 para que podamos ayudarte. Nuestro horario de atención es de Lunes a Viernes de 9 a 19 hs. Recordá tener a mano la información del consumo.",
        "tags": ["consumos_no_reconocidos", "fraude", "atencion_cliente"],
        "keywords": ["consumo desconocido", "fraude", "reclamo", "teléfono atención"],
        "beneficios_clave": ["Soporte rápido ante consumos no reconocidos", "Proceso de reclamo claro"]
    },
    {
        "pregunta": "¿Cómo ver consumos en resúmenes anteriores?",
        "respuesta": "Deberás ingresar a tu cuenta desde nuestro sitio web o desde nuestra APP. En la App: Seleccioná la tarjeta, presioná sobre el producto y después 'Ver todo', buscá la opción 'Histórico de resúmenes'. En la Web: Seleccioná la tarjeta, presioná 'Ver más', deslizá hasta 'Consultas' y buscá 'Histórico de resúmenes'.",
        "tags": ["historial_consumos", "resumen_anterior", "gestion_cuenta"],
        "keywords": ["consumos anteriores", "histórico de resúmenes", "app", "web"],
        "beneficios_clave": ["Acceso al historial de consumos", "Control del gasto a lo largo del tiempo"]
    },
    {
        "pregunta": "¿Cómo aparecen las compras en moneda extranjera?",
        "respuesta": "Los consumos en el exterior en cualquier moneda extranjera aparecen en tu resumen en dólares estadounidenses.",
        "tags": ["moneda_extranjera", "compras_exterior", "resumen_cuenta"],
        "keywords": ["compras en dólares", "consumos internacionales", "moneda extranjera"],
        "beneficios_clave": ["Claridad en la visualización de compras en el exterior"]
    },
    {
        "pregunta": "¿Qué hacer si no recibís tu resumen de cuenta?",
        "respuesta": "Consultalo online. Desde la App: Seleccioná la tarjeta, presioná 'Ver todo', buscá 'Histórico de resúmenes'. Desde la Web: Seleccioná la tarjeta, hacé clic en 'Ver más', deslizá hasta 'Consultas' y seleccioná 'Histórico de resúmenes'. Podrás ver los últimos 12 resúmenes. Si no podés descargarlo, contactate al 0810-9999-627 de Lunes a Viernes de 9 a 19 hs.",
        "tags": ["problemas_resumen", "consulta_online", "atencion_cliente"],
        "keywords": ["no recibo resumen", "descargar resumen", "histórico", "teléfono de ayuda"],
        "beneficios_clave": ["Múltiples opciones para consultar el resumen", "Soporte en caso de problemas"]
    },
    {
        "pregunta": "¿Por qué no recibiste tu resumen?",
        "respuesta": "Solo se genera si realizaste un consumo o tenés saldo pendiente en el período. Revisá tu casilla de correo, incluyendo la carpeta de Spam.",
        "tags": ["resumen_cuenta", "motivo_no_recepcion", "email"],
        "keywords": ["no llega resumen", "consumo pendiente", "spam"],
        "beneficios_clave": ["Aclaración sobre la emisión del resumen", "Consejos para encontrar el resumen"]
    },
    {
        "pregunta": "¿Dónde veo mis límites y disponibles?",
        "respuesta": "Podés conocer tu límite y disponible ingresando a tu cuenta. Desde la Web: Seleccioná el producto, presioná 'Ver más', luego en 'Consultas', seleccioná 'límites y disponibles'. Desde la App: Seleccioná el producto, luego el botón 'Ver todo' y por último 'Límites y disponibles'.",
        "tags": ["limites_disponible", "gestion_cuenta", "informacion_financiera"],
        "keywords": ["límite de crédito", "disponible", "consultar límite", "app", "web"],
        "beneficios_clave": ["Fácil acceso a la información de límites", "Control sobre la capacidad de compra"]
    },
    {
        "pregunta": "¿Qué diferencia hay entre límite y disponible?",
        "respuesta": "El límite es el monto de crédito aprobado para tu tarjeta y el disponible es el importe real hasta el cual el sistema autoriza a gastar para compras en un pago o en cuotas.",
        "tags": ["definicion_financiera", "limite_credito", "disponible"],
        "keywords": ["límite", "disponible", "crédito aprobado", "gasto autorizado"],
        "beneficios_clave": ["Claridad en los conceptos financieros"]
    },
    {
        "pregunta": "Quiero aumentar mi límite",
        "respuesta": "Sí, podés, pero está sujeto a aprobación crediticia. Desde la App: Seleccioná la tarjeta, presioná sobre el producto y después 'Ver todo', buscá la opción 'Aumento de límite'. Desde la Web: Seleccioná la tarjeta, presioná 'Ver más', deslizá hasta 'Operaciones' y buscá 'Aumento de límite'.",
        "tags": ["aumento_limite", "solicitud_credito", "gestion_cuenta"],
        "keywords": ["aumentar límite", "solicitud de límite", "aprobación crediticia", "app", "web"],
        "beneficios_clave": ["Posibilidad de aumentar el límite", "Proceso de solicitud claro"]
    },
    {
        "pregunta": "¿Cómo puedo dar de baja un adicional?",
        "respuesta": "Podés hacerlo comunicándote con nosotros al 0810-9999-627. Nuestro horario de atención es de Lunes a Viernes de 9 a 19 hs.",
        "tags": ["baja_adicional", "atencion_cliente", "tarjetas_adicionales"],
        "keywords": ["dar de baja adicional", "cancelar tarjeta adicional", "teléfono de contacto"],
        "beneficios_clave": ["Facilidad para gestionar tarjetas adicionales"]
    },
    {
        "pregunta": "Me robaron o extravié mi tarjeta",
        "respuesta": "Desde Argentina: Comunicate con nosotros al 0810-9999-627. Desde el exterior: Si estás fuera de Argentina, debés comunicarte al 4340-5656 y solicitar el cobro revertido.",
        "tags": ["robo_extravio", "seguridad_tarjeta", "atencion_cliente"],
        "keywords": ["tarjeta robada", "tarjeta extraviada", "denuncia", "teléfono de emergencia"],
        "beneficios_clave": ["Soporte inmediato en caso de robo o extravío", "Números de contacto para el exterior"]
    },
    {
        "pregunta": "¿Cómo habilito mis tarjetas para viajar al exterior?",
        "respuesta": "Habilitar tus tarjetas para viajar al exterior es muy sencillo. Desde la Web: Ingresá en el menú Inicio, seleccioná 'Ver más', buscá 'Aviso de viaje', completá los datos y seleccioná las tarjetas a habilitar. Desde la App: Seleccioná el producto, 'Ver todo', buscá 'Aviso de viaje', completá los datos y seleccioná las tarjetas. Recordá que también podés habilitar a tus tarjetas adicionales.",
        "tags": ["viajes_exterior", "habilitacion_tarjeta", "gestion_tarjeta"],
        "keywords": ["viajar", "tarjeta internacional", "habilitar tarjeta", "aviso de viaje", "app", "web"],
        "beneficios_clave": ["Proceso sencillo para habilitar tarjetas en el exterior", "Funcionalidad para tarjetas adicionales"]
    },
    {
        "pregunta": "¿Dónde puedo abonar el resumen de cuenta?",
        "respuesta": "Tu resumen podés abonarlo en: cajas de locales Disco, Jumbo, Easy o Vea (efectivo o débito Visa sin cargo); con débito a través de la web o APP sin cargo; a través de Pagos Link, Pago mis cuentas; Cajeros Link y Banelco; Pago Fácil y BAPRO (con resumen). Consultar costos asociados a las transacciones.",
        "tags": ["medios_pago", "pago_resumen", "canales_pago"],
        "keywords": ["pagar resumen", "dónde pagar", "efectivo", "débito", "Pago Fácil", "Pagos Link", "Pago mis cuentas"],
        "beneficios_clave": ["Múltiples opciones para pagar el resumen", "Flexibilidad en los métodos de pago"]
    },
    {
        "pregunta": "¿Cómo puedo pagar mis consumos en dólares?",
        "respuesta": "Para pagar consumos en moneda extranjera deberás: Realizar una transferencia a la cuenta CBU: 3220001812000016740030, ALIAS: PAGO.USD.CENCOSUD. Validá los datos: CUIL: 30-59036076-3, Titular: Cencosud S.A. Debes ser titular de la caja de ahorro en dólares y de la Tarjeta Cencosud. El pago debe ser desde el día posterior al cierre hasta el primer vencimiento, solo días hábiles y se acredita en 48 horas hábiles. Para cancelación en pesos, descontar impuestos por consumos en moneda extranjera, que se reintegrarán en el próximo resumen. Si el pago es parcial, la devolución de impuestos corresponderá al monto pagado. Si estás adherido a pago automático, realizá el stop debit 4 días antes del vencimiento.",
        "tags": ["pago_dolares", "moneda_extranjera", "transferencia_bancaria"],
        "keywords": ["pagar en dólares", "consumos exterior", "transferencia", "CBU", "stop debit"],
        "beneficios_clave": ["Proceso claro para pago en dólares", "Información detallada sobre la gestión de impuestos"]
    },
    {
        "pregunta": "¿Qué opciones de financiación tengo?",
        "respuesta": "Podrás financiar tus consumos en pesos o dólares hasta en 24 cuotas (Cuotificación de consumo) o refinanciar el saldo de tu resumen, abonando el pago mínimo (Plan Cuotas) desde la web o la APP. Recordá hacerlo antes del próximo cierre de tu resumen. El otorgamiento está sujeto a aprobación crediticia. También podés financiar el saldo total más cuotas pendientes llamando al 0810-9999-627 de Lunes a Viernes de 9hs a 19hs, antes del próximo cierre de tu resumen, sujeto a aprobación.",
        "tags": ["financiacion", "cuotas", "planes_pago"],
        "keywords": ["financiar compras", "cuotificación", "plan cuotas", "pagar en cuotas", "refinanciar"],
        "beneficios_clave": ["Amplias opciones de financiación", "Flexibilidad para gestionar pagos"]
    },
    {
        "pregunta": "Si compro en cuotas ¿Qué interés tengo?",
        "respuesta": "Los intereses dependen de las promociones vigentes y podés consultarlas en el comercio donde quieres realizar la compra.",
        "tags": ["intereses", "cuotas", "promociones"],
        "keywords": ["intereses en cuotas", "promociones vigentes", "tasa de interés"],
        "beneficios_clave": ["Transparencia sobre la aplicación de intereses"]
    },
    {
        "pregunta": "¿Qué es Pago Automático?",
        "respuesta": "Es el servicio que permite pagar tu resumen de la tarjeta de crédito Cencopay en forma automática a través de un débito de una cuenta bancaria. Podrás optar por abonar el pago mínimo o el total, y elegir la fecha de cobro que podrá ser la fecha de vencimiento o Plazo Extra-Intereses (una semana después del vencimiento).",
        "tags": ["pago_automatico", "debito_automatico", "comodidad"],
        "keywords": ["pago automático", "débito bancario", "pago mínimo", "pago total", "vencimiento"],
        "beneficios_clave": ["Comodidad en el pago automático", "Opciones de monto y fecha de cobro"]
    },
    {
        "pregunta": "¿Puedo utilizar la cuenta bancaria de otra persona para el pago automático?",
        "respuesta": "No, el titular de la cuenta bancaria debe ser el mismo titular de la tarjeta de crédito Cencopay para poder realizar el pago automático.",
        "tags": ["pago_automatico", "titularidad_cuenta", "requisitos"],
        "keywords": ["cuenta de terceros", "pago automático", "titular tarjeta"],
        "beneficios_clave": ["Claridad en los requisitos de titularidad para el pago automático"]
    },
    {
        "pregunta": "¿Cómo hago para adherirme al pago automático?",
        "respuesta": "Podés adherirte ingresando a tu cuenta desde nuestro sitio web o desde la APP. Desde la Web: Seleccioná el producto, presioná 'Ver más', ingresá a 'Operaciones' y hacé click en 'Pago Automático'. Desde la App: Seleccioná el producto, buscá 'Ver todo' dentro del menú y elegí 'Pago Automático'.",
        "tags": ["adhesion_pago_automatico", "proceso_online", "gestion_cuenta"],
        "keywords": ["adherirse pago automático", "activar pago automático", "web", "app"],
        "beneficios_clave": ["Proceso de adhesión sencillo y accesible"]
    },
    {
        "pregunta": "¿Cuál es la diferencia entre la fecha de cierre y de vencimiento?",
        "respuesta": "La fecha de vencimiento es aquella que indica hasta cuándo se puede abonar el resumen de cuenta, y contás con una segunda fecha de vencimiento con intereses. La fecha de cierre señala el día hasta el cual los consumos efectuados ingresarán en el mismo resumen de cuenta.",
        "tags": ["fechas_facturacion", "cierre_vencimiento", "intereses"],
        "keywords": ["fecha de cierre", "fecha de vencimiento", "segundo vencimiento", "intereses"],
        "beneficios_clave": ["Claridad sobre las fechas importantes del resumen"]
    },
    {
        "pregunta": "¿Dónde veo las fechas de cierre y vencimiento de mi tarjeta?",
        "respuesta": "Podés ver tu cierre y vencimiento actual y de la siguiente facturación en tu resumen de cuenta mensual desde la web o la APP.",
        "tags": ["fechas_facturacion", "consulta_online", "resumen_cuenta"],
        "keywords": ["ver fechas", "cierre", "vencimiento", "resumen mensual"],
        "beneficios_clave": ["Fácil acceso a las fechas de facturación"]
    },
    {
        "pregunta": "¿Cuál es la diferencia entre la Fecha de Vencimiento y la fecha de Plazo Extra?",
        "respuesta": "La diferencia es que podés diferir el pago de tu resumen de cuenta en una segunda instancia. El Plazo Extra-intereses incluye los intereses compensatorios y punitorios calculados desde el vencimiento de la tarjeta.",
        "tags": ["plazo_extra", "intereses_financieros", "pago_diferido"],
        "keywords": ["plazo extra", "vencimiento", "intereses compensatorios", "intereses punitorios", "pago diferido"],
        "beneficios_clave": ["Flexibilidad para el pago con plazo extra"]
    },
    {
        "pregunta": "¿Qué intereses se le cobra en caso de dejar saldos financiando?",
        "respuesta": "Si pagás el total del resumen antes del vencimiento, no se te cobrará ningún interés. Si no pagás a tiempo, se generarán intereses de financiación (sobre el saldo impago), intereses compensatorios (sobre saldos pagados fuera de término) e intereses punitorios (si no se abona el pago mínimo). Los intereses del Plazo Extra se aplican si decidís diferir el pago.",
        "tags": ["intereses_financieros", "saldo_impago", "tipos_intereses"],
        "keywords": ["intereses financiación", "intereses compensatorios", "intereses punitorios", "saldo financiando", "pago fuera de término"],
        "beneficios_clave": ["Transparencia sobre los tipos de intereses aplicados"]
    },
    {
        "pregunta": "Quiero comprar ¿Cuál es mi disponible?",
        "respuesta": "Podés consultar tu disponible desde la web o app ingresando con tu usuario y contraseña, el mismo lo verás en la pantalla de Inicio.",
        "tags": ["disponible_compra", "consulta_saldo", "gestion_cuenta"],
        "keywords": ["disponible para compras", "consultar disponible", "límite", "app", "web"],
        "beneficios_clave": ["Fácil acceso al disponible para compras"]
    },
    {
        "pregunta": "¿Qué necesito para poder adherir un débito automático al pago de un producto/servicio?",
        "respuesta": "Podés solicitarlo en el momento de adquirir el producto o servicio directamente con el comercio.",
        "tags": ["debito_automatico", "adhesion", "productos_servicios"],
        "keywords": ["débito automático", "adherir servicio", "comercio"],
        "beneficios_clave": ["Sencillez en la adhesión de débitos automáticos"]
    },
    {
        "pregunta": "¿Si decido darme de baja al débito, cómo la tramito?",
        "respuesta": "Si la adhesión la solicitaste oportunamente a través del mismo comercio, deberás comunicarte con ellos para notificarlos de tu decisión.",
        "tags": ["baja_debito", "cancelacion_servicio", "comercio"],
        "keywords": ["dar de baja débito", "cancelar servicio", "comercio"],
        "beneficios_clave": ["Proceso de baja de débito claro"]
    },
    {
        "pregunta": "El cajero no me entregó el dinero",
        "respuesta": "Contactate con nosotros accediendo a tu cuenta, seleccionando tu Cencopay, el motivo 'Mi Cuenta Cencopay' y luego el submotivo 'El cajero no me entregó el dinero'. Asegurate de incluir: Ubicación y nombre del cajero, fecha y hora de la transacción, últimos 4 números de la tarjeta. Podrás ver el estado de tu gestión en 'Seguimiento de gestiones'.",
        "tags": ["problemas_cajero", "retiro_efectivo", "reclamo"],
        "keywords": ["cajero sin dinero", "problema cajero", "reclamo", "seguimiento gestión"],
        "beneficios_clave": ["Soporte para problemas con cajeros", "Seguimiento del reclamo"]
    },
    {
        "pregunta": "¿Tiene costo abrir mi Cuenta digital?",
        "respuesta": "Es totalmente gratis.",
        "tags": ["costos_cuenta", "gratuidad", "cuenta_digital"],
        "keywords": ["costo cuenta", "cuenta gratis", "cuenta digital"],
        "beneficios_clave": ["Apertura de cuenta sin costo"]
    },
    {
        "pregunta": "¿Qué es una tarjeta prepaga MasterCard de Cuenta digital?",
        "respuesta": "La tarjeta prepaga MasterCard es internacional y te permite realizar compras en cualquier comercio del mundo. Podrás hacer uso tanto de su formato físico como virtual, y utilizará el saldo disponible en tu cuenta.",
        "tags": ["tarjeta_prepaga", "mastercard", "cuenta_digital"],
        "keywords": ["tarjeta prepaga", "MasterCard", "tarjeta internacional", "formato físico", "formato virtual"],
        "beneficios_clave": ["Versatilidad para compras nacionales e internacionales", "Doble formato (físico y virtual)"]
    },
    {
        "pregunta": "¿Cómo pido mi tarjeta física?",
        "respuesta": "Para pedirla, seguí los pasos. Desde la App: Presioná sobre tu Cuenta digital, 'Ver todo', 'Solicitar tarjeta física', ingresá tu dirección y validá. Desde la Web: Seleccioná tu Cuenta digital, presioná 'Ver más', 'Solicitar tarjeta física', ingresá tu dirección y validá.",
        "tags": ["solicitud_tarjeta", "tarjeta_fisica", "proceso_online"],
        "keywords": ["pedir tarjeta física", "solicitar tarjeta", "app", "web", "envío tarjeta"],
        "beneficios_clave": ["Proceso de solicitud de tarjeta física sencillo y online"]
    },
    {
        "pregunta": "¿Qué diferencia hay entre tarjeta virtual y tarjeta física?",
        "respuesta": "Tarjeta virtual: Es una tarjeta 100% digital, para compras en línea y suscripciones (Netflix, Spotify). Tarjeta física: Es una tarjeta de plástico para compras en establecimientos y retiros de efectivo en cajeros.",
        "tags": ["tipos_tarjeta", "tarjeta_virtual", "tarjeta_fisica"],
        "keywords": ["tarjeta virtual", "tarjeta física", "compras online", "retiros cajero", "usos tarjeta"],
        "beneficios_clave": ["Claridad en las diferencias de uso de las tarjetas"]
    },
    {
        "pregunta": "¿Puedo pausar mi tarjeta?",
        "respuesta": "Sí, podés hacerlo solo desde la APP. Seleccioná tu Cuenta Digital, 'Ver todos', ingresá a 'Pausar tarjeta'. Seleccioná la tarjeta (digital o física). En la pantalla, encontrarás 'Pausar tarjeta' y 'Denunciar tarjeta'. Desde la web solo podrás denunciar tu tarjeta (no pausarla) siguiendo los pasos: Seleccioná tu Cuenta Digital, deslizá hasta 'tarjetas de la cuenta', seleccioná la tarjeta y presioná el icono superior derecho, 'denunciar tarjeta'. Una vez finalizada la gestión, la tarjeta queda bloqueada.",
        "tags": ["pausar_tarjeta", "seguridad_tarjeta", "bloqueo_temporal"],
        "keywords": ["pausar tarjeta", "desactivar temporalmente", "bloqueo", "app", "denunciar tarjeta"],
        "beneficios_clave": ["Control temporal sobre el uso de la tarjeta", "Opción de pausado para mayor seguridad"]
    },
    {
        "pregunta": "¿Qué diferencia hay entre denunciar y pausar?",
        "respuesta": "Pausar una tarjeta la desactiva temporalmente, impidiendo compras (excepto pagos automáticos) y permitiendo reactivarla cuando quieras. Denunciar es una medida de seguridad que inhabilita la tarjeta definitivamente, pero podemos ayudarte a obtener una nueva.",
        "tags": ["seguridad_tarjeta", "pausar_vs_denunciar", "proteccion"],
        "keywords": ["pausar tarjeta", "denunciar tarjeta", "bloqueo temporal", "inhabilitar definitivamente", "seguridad"],
        "beneficios_clave": ["Claridad en las opciones de seguridad de la tarjeta", "Soporte para obtener una nueva tarjeta"]
    },
    {
        "pregunta": "No recibí mi tarjeta física",
        "respuesta": "Si no recibiste tu tarjeta en 15 días, tranqui! Recordá que los tiempos de entrega pueden variar según donde te encuentres, podés seguir el estado del envío desde la sección Seguimiento de gestiones. Si ha pasado más del tiempo indicado y tenes alguna pregunta, no dudes en contactarnos a través del centro de ayuda ¡Tu tranquilidad es lo más importante para nosotros!",
        "tags": ["envio_tarjeta", "demora_entrega", "seguimiento"],
        "keywords": ["tarjeta no recibida", "demora envío", "seguimiento entrega", "centro de ayuda"],
        "beneficios_clave": ["Información sobre el estado del envío", "Soporte en caso de demoras"]
    },
    {
        "pregunta": "No encuentro mi tarjeta",
        "respuesta": "Si no encuentras tu tarjeta, ¡No te preocupes! Podés desactivarla de forma temporal de la siguiente manera: Seleccioná tu CencoPay en la parte superior del Inicio. Deslizá hacia abajo hasta la sección de 'Tarjetas de la cuenta'. Seleccioná la tarjeta que desees pausar y presioná 'Ver datos'. Presioná el botón 'Pausar tarjeta'. ¡Listo! Tu tarjeta quedará desactivada y no podrá ser utilizada hasta que la vuelvas a activar. Si no la encontras, te sugerimos que la denuncies. Esto nos ayudará a tomar las precauciones adecuadas para proteger tu cuenta y prevenir cualquier uso indebido. ¡Tu seguridad es nuestra prioridad!.",
        "tags": ["tarjeta_extraviada", "pausar_tarjeta", "seguridad"],
        "keywords": ["tarjeta perdida", "no encuentro tarjeta", "pausar", "denunciar", "seguridad cuenta"],
        "beneficios_clave": ["Control temporal de la tarjeta", "Opciones de seguridad ante extravío"]
    },
    {
        "pregunta": "¿Se puede realizar compras en moneda extranjera?",
        "respuesta": "Sí, es importante que sepas que los consumos se debitan en pesos e incluyen los impuestos y cargos correspondientes. Utilizaremos el tipo de cambio BNA vendedor minorista publicado al cierre del día anterior a la fecha de la operación sumándole los impuestos asociados. Si queres consultar la cotización actualizada podés ingresar a la página del Banco de la Nación Argentina. Para revisar la cotización de un movimiento que ya realizaste puedes hacerlo ingresando al detalle de movimientos.",
        "tags": ["compras_internacionales", "moneda_extranjera", "cotizacion"],
        "keywords": ["comprar en dólares", "compras exterior", "tipo de cambio", "impuestos", "cotización BNA"],
        "beneficios_clave": ["Posibilidad de compras internacionales", "Transparencia en la aplicación de impuestos y tipo de cambio"]
    },
    {
        "pregunta": "¿Cómo visualizo mis movimientos?",
        "respuesta": "Es muy simple. Seleccioná tu Cuenta digital en la parte superior del inicio. Deslizá hacia abajo hasta la sección de 'últimos movimientos'. Si queres ver el listado completo, presioná 'ver todos'. Para ver el detalle de una transacción, elegí el movimiento que desees.",
        "tags": ["movimientos_cuenta", "consulta_online", "gestion_cuenta"],
        "keywords": ["ver movimientos", "historial de transacciones", "cuenta digital", "app", "web"],
        "beneficios_clave": ["Fácil acceso al historial de movimientos", "Control detallado de transacciones"]
    },
    {
        "pregunta": "¿Qué pasa si no veo los movimientos realizados?",
        "respuesta": "Recordá que algunas transacciones pueden demorar hasta 24 hs en mostrarse. Si pasaron más de 24hs: Contactate con nosotros a través del centro de ayuda.",
        "tags": ["movimientos_pendientes", "demora_transaccion", "soporte"],
        "keywords": ["movimientos no aparecen", "transacción demorada", "centro de ayuda"],
        "beneficios_clave": ["Aclaración sobre tiempos de procesamiento", "Soporte en caso de problemas"]
    },
    {
        "pregunta": "¿Qué pasa si veo un movimiento que no hice?",
        "respuesta": "Pausá tu tarjeta desde la APP: Ingresá en Productos. Deslizá hacia abajo hasta llegar a la sección de 'Tarjetas de la cuenta' y pausá tus plásticos virtuales y físicos. Contactate con nosotros: Podés hacerlo desde aquí donde deberás elegir tu Cuenta digital, el motivo 'Seguridad' y luego el submotivo 'Veo una operación que yo no realicé'. ¡Es importante! Asegúrate de incluir toda la información sobre el movimiento que no reconoces. Podrás visualizar el estado de tu gestión desde la sección seguimiento de gestiones.",
        "tags": ["movimiento_no_reconocido", "fraude", "seguridad", "pausar_tarjeta"],
        "keywords": ["movimiento desconocido", "fraude", "pausar tarjeta", "reportar operación", "seguimiento gestión"],
        "beneficios_clave": ["Acciones inmediatas para proteger la cuenta", "Soporte y seguimiento de reclamos"]
    },
    {
        "pregunta": "No pude pagar con mi Cuenta digital",
        "respuesta": "Si tu tarjeta no funciona para realizar compras, te sugerimos que verifiques los siguientes puntos: Asegúrate de contar con suficiente saldo disponible en tu cuenta. Verifica que tu tarjeta no esté pausada. Si estás intentando utilizar tu tarjeta física en un establecimiento, verifica que el chip o la banda magnética no estén dañados. Si estás intentando realizar una compra por internet, verifica tu conexión.",
        "tags": ["problemas_pago", "cuenta_digital", "solucion_problemas"],
        "keywords": ["pago rechazado", "tarjeta no funciona", "saldo insuficiente", "tarjeta pausada", "problemas chip"],
        "beneficios_clave": ["Guía de solución de problemas de pago", "Consejos para asegurar transacciones exitosas"]
    },
    {
        "pregunta": "¿Qué es tu dinero en cuenta?",
        "respuesta": "Es el saldo disponible que tenés en tu cuenta, con el que podés realizar pagos, consumos, transferencias y extracciones.",
        "tags": ["definicion_saldo", "cuenta_digital", "usos_dinero"],
        "keywords": ["dinero en cuenta", "saldo disponible", "pagos", "consumos", "transferencias", "extracciones"],
        "beneficios_clave": ["Claridad sobre el saldo disponible y sus usos"]
    },
    {
        "pregunta": "¿Cómo ingreso dinero en mi cuenta?",
        "respuesta": "Consulta todas las formas que tenes para añadir dinero en tu cuenta: Posicionate sobre tu Cuenta digital en la parte superior del inicio y presiona 'Ver detalle'. En los botones principales, encontraras la opción de 'ingresar dinero'. En la pantalla que se muestra, se encuentra toda la información necesaria para poder realizar el ingreso de dinero a tu cuenta.",
        "tags": ["ingreso_dinero", "recarga_cuenta", "metodos_pago"],
        "keywords": ["ingresar dinero", "cargar cuenta", "formas de ingreso"],
        "beneficios_clave": ["Múltiples opciones para ingresar dinero", "Información detallada sobre el proceso"]
    },
    {
        "pregunta": "¿Cuánto tiempo demora un ingreso de dinero físico?",
        "respuesta": "Los depósitos en efectivo son inmediatos, puedes realizarlos en la línea de cajas en Jumbo, Disco, Vea o en cajeros automáticos. Recordá que en algunos casos puede demorar hasta 72 horas hábiles.",
        "tags": ["ingreso_dinero", "tiempos_acreditacion", "depositos"],
        "keywords": ["depósito efectivo", "tiempo acreditación", "Jumbo", "Disco", "Vea", "cajeros automáticos"],
        "beneficios_clave": ["Claridad sobre los tiempos de acreditación de depósitos"]
    },
    {
        "pregunta": "Se bloqueó mi PIN del cajero",
        "respuesta": "Si se bloqueó tu PIN del cajero deberás acercarte a un cajero automático con tu tarjeta física y seguir las instrucciones.",
        "tags": ["pin_bloqueado", "cajero_automatico", "solucion_problemas"],
        "keywords": ["PIN bloqueado", "cajero", "desbloquear PIN", "tarjeta física"],
        "beneficios_clave": ["Solución rápida para el bloqueo del PIN"]
    },
    {
        "pregunta": "¿Qué puedo hacer con Cuenta digital?",
        "respuesta": "Con Cuenta digital podés disfrutar todos estos beneficios: Realizá pagos y consumos de manera rápida y sencilla. Pedí tu tarjeta prepaga MasterCard y utilizala en miles de comercios. Administrá tus finanzas y llevá el seguimiento de todos tus gastos. ¡Accedé a las promociones exclusivas en nuestras tiendas!",
        "tags": ["beneficios_cuenta_digital", "funcionalidades", "ventajas"],
        "keywords": ["cuenta digital", "pagos", "consumos", "tarjeta prepaga", "administrar finanzas", "promociones"],
        "beneficios_clave": ["Amplia gama de funcionalidades", "Acceso a beneficios y promociones"]
    },
    {
        "pregunta": "¿Qué servicios puedo pagar?",
        "respuesta": "Podrás pagar diversos servicios, como, por ejemplo, servicios de luz, gas, teléfono, municipal, entre tantos más.",
        "tags": ["pago_servicios", "servicios_disponibles", "utilidades"],
        "keywords": ["pagar servicios", "luz", "gas", "teléfono", "municipal"],
        "beneficios_clave": ["Comodidad para pagar una variedad de servicios"]
    },
    {
        "pregunta": "¿Cómo puedo hacer para pagar estos servicios?",
        "respuesta": "Podrás hacerlo desde la APP o web, ingresando con tu usuario y contraseña y seleccionando, dentro del menú, la opción de servicios/pago de servicios.",
        "tags": ["pago_servicios", "proceso_online", "app_web"],
        "keywords": ["cómo pagar servicios", "app", "web", "pago de servicios"],
        "beneficios_clave": ["Facilidad y accesibilidad para el pago de servicios"]
    },
    {
        "pregunta": "¿Qué servicios puedo recargar?",
        "respuesta": "Podrás realizar la recarga de celulares, SUBE y DIRECTV, MIDE sin importar que no sean tuyos.",
        "tags": ["recargas", "servicios_disponibles", "comodidad"],
        "keywords": ["recargar celular", "SUBE", "DIRECTV", "MIDE", "recargas"],
        "beneficios_clave": ["Amplia variedad de servicios de recarga", "Flexibilidad para recargar a terceros"]
    },
    {
        "pregunta": "¿Dónde veo el detalle de una recarga?",
        "respuesta": "Desde el Inicio ingresá al tipo de recarga que quieras consultar (celular, SUBE, MIDE o DIRECTV). Deslizá hacia abajo hasta llegar a la sección 'Últimas recargas'. Ahí encontrarás un registro de todas las recargas que hayas realizado. Seleccioná la recarga que quieras consultar y accedé a la información detallada, como el número de celular recargado, el importe cargado y la fecha de la recarga.",
        "tags": ["detalle_recarga", "historial_recargas", "consulta_online"],
        "keywords": ["ver recargas", "historial recargas", "celular", "SUBE", "DIRECTV", "MIDE"],
        "beneficios_clave": ["Acceso fácil al detalle de recargas", "Control sobre las recargas realizadas"]
    },
    {
        "pregunta": "¿La recarga es inmediata?",
        "respuesta": "Sí, el pago puede acreditarse en un plazo máximo de 72 hs ya que pueden observarse demoras que responden a la demanda que presenten los distintos servicios.",
        "tags": ["recargas", "tiempos_acreditacion", "demoras"],
        "keywords": ["recarga inmediata", "tiempo acreditación", "demoras recarga"],
        "beneficios_clave": ["Claridad sobre los tiempos de acreditación de recargas"]
    },
    {
        "pregunta": "¿Dónde veo los comprobantes de pago?",
        "respuesta": "Para ver y descargar tus comprobantes de pago tenés que realizar lo siguiente: Desde el inicio ingresá en la opción 'Pago de servicios'. Deslizá hacia abajo hasta llegar a la sección 'Últimos Pagos'. Buscá el pago específico y seleccionálo. Descargá el comprobante asociado.",
        "tags": ["comprobantes_pago", "historial_pagos", "descarga"],
        "keywords": ["comprobante de pago", "descargar comprobante", "historial pagos", "pago de servicios"],
        "beneficios_clave": ["Fácil acceso y descarga de comprobantes de pago"]
    },
    {
        "pregunta": "¿Puedo cargar crédito en el celular de cualquier compañía?",
        "respuesta": "Sí, podrás recargar celulares que sean Claro, Movistar, Personal, Tuenti.",
        "tags": ["recargas_celular", "operadoras_disponibles", "compatibilidad"],
        "keywords": ["cargar crédito", "recargar celular", "Claro", "Movistar", "Personal", "Tuenti"],
        "beneficios_clave": ["Amplia compatibilidad con operadoras de celular"]
    },
    {
        "pregunta": "¿Qué medios de pago puedo utilizar?",
        "respuesta": "Podés pagar con tu tarjeta o con el dinero disponible de tu cuenta digital, siempre y cuando sean aceptados por el comercio. Cuando escanees el QR podrás ver todas las opciones de pago disponibles para el pago que intentas realizar.",
        "tags": ["medios_pago", "opciones_pago", "QR"],
        "keywords": ["medios de pago", "tarjeta", "cuenta digital", "pago QR"],
        "beneficios_clave": ["Flexibilidad en los medios de pago", "Visibilidad de opciones de pago con QR"]
    },
    {
        "pregunta": "¿Por qué un pago puede ser rechazado?",
        "respuesta": "Un pago puede ser rechazado por los siguientes motivos: Sin disponible (asegurate que el importe no supere tu disponible, o solicitá aumento de límite si es tarjeta de crédito). Tarjeta inválida (comunicate con nosotros para información sobre el estado de la tarjeta). Cantidad de cuotas inválidas (es posible que el número de cuotas no esté disponible para el método de pago seleccionado).",
        "tags": ["pago_rechazado", "problemas_pago", "solucion_problemas"],
        "keywords": ["pago denegado", "sin disponible", "tarjeta inválida", "cuotas inválidas", "aumento de límite"],
        "beneficios_clave": ["Claridad sobre los motivos de rechazo de pago", "Guía para solucionar problemas de pago"]
    },
    {
        "pregunta": "Pago con QR",
        "respuesta": "Con la APP CENCOPAY vas a poder pagar con código QR, solo tenes que ingresar teniendo el nivel máximo de seguridad. Buscá la opción pagar y escaneá el código que te indique el comercio. Allí podrás ver el importe, la cantidad de cuotas y el importe por cada cuota. Elegí la tarjeta con la que vas a pagar y confirmá el pago. ¡Listo! En la pantalla podrás corroborar la información de la transacción.",
        "tags": ["pago_QR", "proceso_pago", "seguridad"],
        "keywords": ["pagar con QR", "código QR", "app cencopay", "seguridad", "confirmar pago"],
        "beneficios_clave": ["Proceso de pago QR sencillo y seguro", "Visibilidad de detalles de la transacción"]
    },
    {
        "pregunta": "¿Cómo funcionan los descuentos con pagos con QR?",
        "respuesta": "Los descuentos correspondientes al pago con QR se verán reflejados en el siguiente o subsiguiente resumen de cuenta de la tarjeta seleccionada al momento de realizar el pago.",
        "tags": ["descuentos_QR", "beneficios", "acreditacion_descuentos"],
        "keywords": ["descuentos QR", "promociones", "resumen de cuenta", "acreditación descuentos"],
        "beneficios_clave": ["Claridad sobre la aplicación de descuentos por QR"]
    },
    {
        "pregunta": "¿Cómo realizo el pago con QR?",
        "respuesta": "Vas a poder comprar en todos los locales que acepten pago QR. Pagar con QR es muy sencillo. Comentale al vendedor que vas a pagar con QR, te informará la financiación posible y podrás elegir. Una vez en la APP, entrá a la sección de pago con QR (botón central del menú) y escaneá el código. Allí verás el importe, cuotas e importe por cuota. Elegí la tarjeta y confirmá. ¡Listo! En la pantalla podrás corroborar la información.",
        "tags": ["proceso_pago_QR", "pasos_QR", "comodidad"],
        "keywords": ["pago con QR", "cómo pagar", "locales con QR", "financiación QR", "app"],
        "beneficios_clave": ["Guía paso a paso para el pago QR", "Comodidad en la compra"]
    },
    {
        "pregunta": "¿Qué necesito para pagar con QR?",
        "respuesta": "Necesitas tener descargada la app en un teléfono celular o Tablet que posea una cámara integrada y tener el máximo nivel de seguridad.",
        "tags": ["requisitos_QR", "app", "seguridad"],
        "keywords": ["requisitos pago QR", "app", "celular", "tablet", "cámara", "nivel de seguridad"],
        "beneficios_clave": ["Claridad en los requisitos para usar el pago QR"]
    },
    {
        "pregunta": "¿Qué es una cuenta remunerada?",
        "respuesta": "Es tu cuenta Cencopay que te permite obtener rendimientos diarios.",
        "tags": ["definicion_producto", "cuenta_remunerada", "rendimientos"],
        "keywords": ["cuenta remunerada", "rendimientos diarios", "inversión"],
        "beneficios_clave": ["Generación de rendimientos diarios", "Optimización del dinero en cuenta"]
    },
    {
        "pregunta": "¿Debo tener algo más en cuenta?",
        "respuesta": "Sí, que no se asegura ni garantiza el resultado de la inversión. SBS Asset Management S.A.S.G.F.C.I. Actuará como Sociedad Gerente y Banco de Valores S.A. actuará como Sociedad Depositaria. El valor de la cuota parte será neto de gastos ordinarios de gestión y de los honorarios de la sociedad gerente y la sociedad depositaria. No existen honorarios de éxito. Las inversiones en cuotapartes del fondo no constituyen depósito en el Banco de Valores S.A. ni cuenta con garantías. Banco de Valores S.A. se encuentra impedido de asumir compromiso sobre el mantenimiento del capital, rendimiento o liquidez.",
        "tags": ["informacion_legal", "riesgos_inversion", "FCI"],
        "keywords": ["riesgos inversión", "FCI", "SBS Asset Management", "Banco de Valores", "cuotapartes", "garantías"],
        "beneficios_clave": ["Transparencia sobre los riesgos y condiciones de la inversión"]
    },
    {
        "pregunta": "¿Cómo funciona el rendimiento?",
        "respuesta": "Los saldos a remunerar se acreditan en la cuenta de Lunes a Viernes, solo días hábiles. Si invertís el dinero de Lunes a Jueves antes de las 22 hs, ves el saldo remunerado a las 48 hs hábiles. Si invertís el día Jueves después de las 22 hs, Viernes, Sábado o Domingo hasta las 18 hs, ves el saldo remunerado el día martes. Si invertís el domingo después de las 18 hs, ves el saldo remunerado el día miércoles. Los saldos remunerados son acreditados a las 20 hs aproximadamente, pudiendo extenderse hasta las 22 hs. Los movimientos podés verlos desde la sección 'Rendimientos'.",
        "tags": ["rendimiento_cuenta", "acreditacion", "tiempos_procesamiento"],
        "keywords": ["cómo funciona rendimiento", "acreditación rendimientos", "días hábiles", "horarios", "movimientos"],
        "beneficios_clave": ["Claridad sobre el funcionamiento y tiempos de acreditación de rendimientos"]
    },
    {
        "pregunta": "¿Cómo se calcula el rendimiento?",
        "respuesta": "El rendimiento se calcula mediante la fórmula (TNA/100/365) x saldo en cuenta. La TNA informada la podés encontrar en la pantalla de inicio arriba de tu dinero disponible en cuenta digital. El porcentaje anual de rendimiento es estimado y puede variar diariamente, basado en la rentabilidad de los últimos 30 días del Fondo común de inversión. El FCI no garantiza rentabilidades futuras.",
        "tags": ["calculo_rendimiento", "TNA", "FCI"],
        "keywords": ["calcular rendimiento", "TNA", "Fondo común de inversión", "rentabilidad estimada", "variación diaria"],
        "beneficios_clave": ["Transparencia en el cálculo del rendimiento", "Información sobre la TNA"]
    },
    {
        "pregunta": "¿Qué es una cuota parte?",
        "respuesta": "Los FCI dividen la participación de sus inversores en unidades llamadas 'Cuotapartes'. Cuando accedemos a un FCI, lo que estamos haciendo es 'suscribiendo Cuotapartes', es decir, nos hacemos dueños de una porción indivisa del patrimonio del FCI. La cantidad de Cuotapartes que adquirís está determinada por el dinero que tengas invertido y el valor de la Cuotaparte. Cuando 'rescatás Cuotapartes' solicitas que se te entregue el dinero correspondiente de la valuación de tus Cuotapartes.",
        "tags": ["definicion_inversion", "cuotapartes", "FCI"],
        "keywords": ["cuota parte", "FCI", "inversión", "suscribir cuotapartes", "rescatar cuotapartes"],
        "beneficios_clave": ["Claridad en el concepto de cuotapartes y su funcionamiento"]
    },
    {
        "pregunta": "¿Qué es un FCI?",
        "respuesta": "Es un vehículo donde participás junto con otras personas de una herramienta de inversión a través de la cual una Sociedad Gerente (SBS Asset Management S.A.S.G.F.C.I.) profesional y especializada administra el dinero para que genere rendimientos. Los activos en los que invierte el FCI son custodiados por una Sociedad Depositaria (Banco de Valores S.A.). Todos los días ese dinero puede generar rendimientos a partir de una rentabilidad anual estimada que tendrás siempre a la vista.",
        "tags": ["definicion_inversion", "FCI", "sociedad_gerente", "sociedad_depositaria"],
        "keywords": ["FCI", "Fondo común de inversión", "inversión", "SBS Asset Management", "Banco de Valores", "rendimientos"],
        "beneficios_clave": ["Comprensión del funcionamiento de un FCI", "Información sobre los actores involucrados"]
    },
    {
        "pregunta": "¿La cuenta remunerada es segura?",
        "respuesta": "El FCI en el que se invierte tu dinero participa de activos de bajo riesgo.",
        "tags": ["seguridad_inversion", "riesgo_bajo", "FCI"],
        "keywords": ["cuenta remunerada segura", "riesgo de inversión", "FCI", "activos de bajo riesgo"],
        "beneficios_clave": ["Tranquilidad sobre la seguridad de la inversión"]
    },
    {
        "pregunta": "¿Para quiénes está disponible la cuenta remunerada?",
        "respuesta": "Disponible para usuarios desde la APP, con tecnología IOS o Android, asegurando una relación comercial autorizada.",
        "tags": ["disponibilidad", "requisitos_tecnicos", "cuenta_remunerada"],
        "keywords": ["quién puede usar", "cuenta remunerada", "app", "IOS", "Android"],
        "beneficios_clave": ["Claridad sobre la disponibilidad de la cuenta remunerada"]
    },
    {
        "pregunta": "¿Cómo empiezo a generar rendimientos?",
        "respuesta": "Una vez que tengas tu cuenta digital activa, aceptá los términos y condiciones y tu saldo en cuenta comenzará a generar rendimientos diarios.",
        "tags": ["inicio_rendimientos", "activacion_cuenta", "terminos_condiciones"],
        "keywords": ["generar rendimientos", "activar cuenta", "aceptar términos"],
        "beneficios_clave": ["Proceso sencillo para activar rendimientos"]
    },
    {
        "pregunta": "¿Existe algún costo por comenzar a remunerar?",
        "respuesta": "No hay costos asociados cuando utilizás el servicio.",
        "tags": ["costos_inversion", "gratuidad", "cuenta_remunerada"],
        "keywords": ["costo remunerar", "sin costo", "servicio gratuito"],
        "beneficios_clave": ["Servicio de remuneración sin costos adicionales"]
    },
    {
        "pregunta": "¿En qué se diferencia de un Plazo Fijo?",
        "respuesta": "A diferencia de un Plazo Fijo, el servicio de cuenta remunerada permite disponibilidad inmediata del dinero sin trámites ni plazos.",
        "tags": ["comparativa_inversion", "plazo_fijo", "disponibilidad"],
        "keywords": ["diferencia plazo fijo", "disponibilidad inmediata", "sin plazos"],
        "beneficios_clave": ["Mayor flexibilidad y liquidez que un plazo fijo"]
    },
    {
        "pregunta": "¿Cuándo se acreditan los rendimientos?",
        "respuesta": "Los rendimientos se acreditan los días hábiles.",
        "tags": ["acreditacion_rendimientos", "frecuencia"],
        "keywords": ["cuando se acreditan", "días hábiles", "rendimientos"],
        "beneficios_clave": ["Claridad sobre la frecuencia de acreditación de rendimientos"]
    },
    {
        "pregunta": "¿Los fines de semana mi plata sigue generando rendimientos?",
        "respuesta": "Sí los fines de semana tu plata sigue generando rendimientos, este se acumula y se ve reflejado al siguiente día hábil.",
        "tags": ["rendimientos_fines_semana", "acumulacion"],
        "keywords": ["rendimientos fines de semana", "acumulación", "día hábil"],
        "beneficios_clave": ["Continuidad en la generación de rendimientos"]
    },
    {
        "pregunta": "¿Puedo usar mi dinero en cualquier momento?",
        "respuesta": "El saldo siempre estará disponible, sin restricciones temporales.",
        "tags": ["disponibilidad_dinero", "liquidez", "cuenta_remunerada"],
        "keywords": ["usar dinero", "disponibilidad saldo", "sin restricciones"],
        "beneficios_clave": ["Acceso inmediato y sin restricciones al dinero"]
    },
    {
        "pregunta": "¿Cómo funciona una cuenta remunerada?",
        "respuesta": "El saldo en la cuenta se invierte en cuota partes de un FCI y los resultados de los activos en los que invierte el FCI generan rendimiento para vos.",
        "tags": ["funcionamiento_cuenta", "FCI", "rendimientos"],
        "keywords": ["cómo funciona cuenta remunerada", "inversión FCI", "generar rendimiento"],
        "beneficios_clave": ["Explicación clara del funcionamiento de la cuenta remunerada"]
    },
    {
        "pregunta": "¿Para qué sirve la sección de Seguros y Asistencias de la plataforma Cencopay?",
        "respuesta": "Es un centro de operaciones online exclusivo para clientes, disponible 24 horas. Permite ver coberturas contratadas con tu tarjeta de crédito Cencopay, información útil y contratar nuevas coberturas de forma sencilla.",
        "tags": ["seguros", "asistencias", "plataforma_online", "beneficios"],
        "keywords": ["seguros cencopay", "asistencias", "coberturas", "contratar seguro", "plataforma online"],
        "beneficios_clave": ["Gestión online de seguros y asistencias", "Acceso 24/7 a información y contratación"]
    },
    {
        "pregunta": "¿Cómo encuentro un seguro o una asistencia a contratar?",
        "respuesta": "Para encontrar información sobre los productos disponibles a través de la plataforma Tarjeta Cencosud, tenés que ir a la sección Seguros y Asistencias y elegir la opción Contratación. Tenés que contar con un usuario y contraseña de acceso a la plataforma Tarjeta Cencosud.",
        "tags": ["contratacion_seguro", "busqueda_seguro", "plataforma_online"],
        "keywords": ["encontrar seguro", "contratar asistencia", "sección seguros", "usuario y contraseña"],
        "beneficios_clave": ["Proceso guiado para encontrar y contratar seguros"]
    },
    {
        "pregunta": "¿Por qué es importante pensar en la contratación de un seguro o una asistencia?",
        "respuesta": "El seguro y la asistencia son la protección contra los riesgos que afectan a las personas y su patrimonio. A cambio de un pago relativamente pequeño, las personas se protegen contra un retroceso financiero o una pérdida. Es muy importante tener una asistencia y/o un seguro, aunque no necesariamente se haga uso de él.",
        "tags": ["importancia_seguro", "proteccion", "riesgos"],
        "keywords": ["importancia seguro", "protección", "riesgos", "seguridad financiera"],
        "beneficios_clave": ["Conciencia sobre la importancia de la protección financiera"]
    },
    {
        "pregunta": "¿En qué consiste el Seguro de Compra protegida?",
        "respuesta": "Es un seguro para titulares de tarjetas de crédito que protege los bienes adquiridos y abonados con este medio de pago en el caso de robo o daño accidental. Es exclusivo para uso personal del titular de la tarjeta de crédito.",
        "tags": ["seguro_compra", "proteccion_bienes", "robo_daño"],
        "keywords": ["seguro compra protegida", "robo", "daño accidental", "bienes adquiridos", "tarjeta de crédito"],
        "beneficios_clave": ["Protección de compras realizadas con tarjeta de crédito"]
    },
    {
        "pregunta": "¿En qué consiste el seguro de tecnología protegida?",
        "respuesta": "Es un seguro que protege contra el robo o el daño de todos aquellos aparatos electrónicos que incluye la cobertura: celulares, notebooks, netbooks, tablets.",
        "tags": ["seguro_tecnologia", "proteccion_electronicos", "robo_daño"],
        "keywords": ["seguro tecnología protegida", "celulares", "notebooks", "tablets", "robo", "daño"],
        "beneficios_clave": ["Protección de dispositivos electrónicos"]
    },
    {
        "pregunta": "¿En qué consiste la asistencia de electro?",
        "respuesta": "Es una asistencia que protege a electrodomésticos de hasta 10 años de antigüedad ante desperfectos que impiden el correcto funcionamiento. Incluye electrodomésticos como: lavarropas, heladera, calefactor, termotanque/calefón, notebooks/PC, LED/LCD, entre otros.",
        "tags": ["asistencia_electro", "electrodomesticos", "desperfectos"],
        "keywords": ["asistencia electro", "electrodomésticos", "desperfectos", "reparación"],
        "beneficios_clave": ["Protección y asistencia para electrodomésticos"]
    },
    {
        "pregunta": "¿Qué puedo hacer en caso de tener un problema con mi cobertura?",
        "respuesta": "Si la compañía aseguradora no te brinda respuesta, tu siniestro fue rechazado, desconoces el cobro de un seguro o cualquier otro inconveniente relacionado a tu cobertura, podés denunciarlo o consultarlo en la Superintendencia de Seguros de la Nación > Teléfono: 0800-666-8400 > Página Web: www.argentina.gob.ar/superintendencia-de-seguros/consultas-y-denuncias.",
        "tags": ["problemas_cobertura", "reclamo_seguro", "superintendencia_seguros"],
        "keywords": ["problema seguro", "siniestro rechazado", "denunciar seguro", "Superintendencia de Seguros"],
        "beneficios_clave": ["Canales para reclamos y consultas sobre seguros"]
    },
    {
        "pregunta": "¿En qué consiste el seguro de bolso protegido?",
        "respuesta": "Es un seguro que cubre tu bolso/mochila/cartera y su contenido en caso de robo. También ofrece traslado a la clínica más cercana ante el robo.",
        "tags": ["seguro_bolso", "robo_pertenencias", "asistencia"],
        "keywords": ["seguro bolso protegido", "robo bolso", "mochila", "cartera", "contenido", "traslado clínica"],
        "beneficios_clave": ["Protección de pertenencias personales y asistencia en caso de robo"]
    },
    {
        "pregunta": "¿En qué consiste la cobertura PUA?",
        "respuesta": "Es una asistencia que te protege en caso de robo en vía pública, mediante una línea abierta las 24hs recibirás atención, contención y asesoramiento para solucionar la emergencia del robo sufrido.",
        "tags": ["asistencia_PUA", "robo_via_publica", "emergencia"],
        "keywords": ["cobertura PUA", "robo vía pública", "atención 24hs", "asesoramiento"],
        "beneficios_clave": ["Asistencia y soporte en caso de robo en vía pública"]
    },
    {
        "pregunta": "¿Cómo denunciar un siniestro?",
        "respuesta": "Desde el Inicio presioná Seguros y asistencias e ingresá a la opción 'Mis Coberturas', tenes que hacer click sobre la póliza en particular y allí encontrarás toda la información que necesitas.",
        "tags": ["denuncia_siniestro", "proceso_online", "seguros"],
        "keywords": ["denunciar siniestro", "reportar siniestro", "mis coberturas", "póliza"],
        "beneficios_clave": ["Proceso sencillo para denunciar un siniestro"]
    },
    {
        "pregunta": "¿Cómo puedo modificar datos de mi póliza o solicitar una copia de la póliza?",
        "respuesta": "Desde el Inicio presioná Seguros y asistencias. A través de la opción 'Mis Coberturas', buscás la póliza en particular y al desplegar la información encontrarás lo que necesitas.",
        "tags": ["gestion_poliza", "modificar_datos", "copia_poliza"],
        "keywords": ["modificar póliza", "copia póliza", "mis coberturas", "datos seguro"],
        "beneficios_clave": ["Facilidad para gestionar y obtener información de la póliza"]
    },
    {
        "pregunta": "¿Cómo dar de baja mi póliza?",
        "respuesta": "A través de la opción Mis Coberturas, tenés que hacer click sobre la póliza en particular y allí encontrarás toda la información que necesitas.",
        "tags": ["baja_poliza", "cancelacion_seguro", "gestion_seguro"],
        "keywords": ["dar de baja póliza", "cancelar seguro", "mis coberturas"],
        "beneficios_clave": ["Proceso claro para dar de baja una póliza"]
    },
    {
        "pregunta": "¿En qué consiste la asistencia al hogar?",
        "respuesta": "Es una asistencia que cubre urgencias domiciliarias mediante el envío de un especialista como: plomero, cerrajero, electricista, entre otros.",
        "tags": ["asistencia_hogar", "urgencias_domiciliarias", "especialistas"],
        "keywords": ["asistencia hogar", "plomero", "cerrajero", "electricista", "urgencias"],
        "beneficios_clave": ["Soporte para urgencias en el hogar con especialistas"]
    },
    {
        "pregunta": "¿Qué es Crédito en tienda?",
        "respuesta": "Crédito en tienda es una línea de crédito personal otorgada por Cencosud para que puedas comprar en cuotas en nuestras tiendas seleccionadas lo que necesites (excepto alimentos).",
        "tags": ["credito_personal", "compras_cuotas", "tiendas_cencosud"],
        "keywords": ["crédito en tienda", "línea de crédito", "comprar en cuotas", "Cencosud", "tiendas seleccionadas"],
        "beneficios_clave": ["Acceso a crédito para compras en tiendas Cencosud", "Posibilidad de pagar en cuotas"]
    },
    {
        "pregunta": "¿Cómo solicito la baja del préstamo Crédito en Tienda?",
        "respuesta": "Para más información, comunicate con nuestro Centro de Atención al Cliente al 0810-9999-627 de Lunes a Viernes de 9 a 19 hs.",
        "tags": ["baja_prestamo", "credito_tienda", "atencion_cliente"],
        "keywords": ["dar de baja préstamo", "cancelar crédito en tienda", "teléfono de contacto"],
        "beneficios_clave": ["Soporte para la baja del préstamo"]
    },
    {
        "pregunta": "¿Cómo y dónde puedo usarlo?",
        "respuesta": "Podés utilizarlo en los locales seleccionados de Easy, Jumbo, Disco y Vea presentando el token que hayas generado al momento de la solicitud.",
        "tags": ["uso_credito", "comercios_adheridos", "token"],
        "keywords": ["dónde usar crédito", "Easy", "Jumbo", "Disco", "Vea", "token"],
        "beneficios_clave": ["Amplia red de comercios para usar el crédito", "Uso sencillo con token"]
    },
    {
        "pregunta": "¿Cuáles son los requisitos para pedir la línea de crédito?",
        "respuesta": "Para poder solicitar la línea de crédito necesitas tener el documento a mano y un dispositivo con cámara.",
        "tags": ["requisitos_credito", "solicitud_credito", "documentacion"],
        "keywords": ["requisitos línea de crédito", "documento", "dispositivo con cámara"],
        "beneficios_clave": ["Claridad en los requisitos para solicitar la línea de crédito"]
    },
    {
        "pregunta": "¿Las cuotas de los préstamos son fijas?",
        "respuesta": "Sí, las cuotas son fijas y se calculan bajo el Sistema Francés.",
        "tags": ["cuotas_prestamo", "sistema_frances", "financiacion"],
        "keywords": ["cuotas fijas", "préstamos", "Sistema Francés"],
        "beneficios_clave": ["Estabilidad en el monto de las cuotas"]
    },
    {
        "pregunta": "Dónde veo mis movimientos?",
        "respuesta": "Podés consultar tus movimientos desde la App Cencopay o la Web. Seleccioná el producto 'Crédito en Tienda' para visualizar: Detalle de tus movimientos. Monto otorgado y disponible. Fecha de vencimiento. Lugares de Pago.",
        "tags": ["movimientos_credito", "consulta_online", "gestion_credito"],
        "keywords": ["ver movimientos crédito", "app cencopay", "web", "monto otorgado", "disponible", "fecha vencimiento"],
        "beneficios_clave": ["Acceso fácil al detalle de movimientos del crédito", "Control de la línea de crédito"]
    },
    {
        "pregunta": "¿Dónde puedo realizar los pagos?",
        "respuesta": "Podrás abonar el resumen de cuenta de manera online a través de nuestra app/web, en los sitios pagomiscuentas, link pagos o de manera presencial en la línea de caja de los locales de Disco, Jumbo, Vea e Easy, Banelco, Red-Link y Pago Fácil.",
        "tags": ["medios_pago", "pago_prestamo", "canales_pago"],
        "keywords": ["dónde pagar préstamo", "pago online", "pagomiscuentas", "link pagos", "locales", "Pago Fácil"],
        "beneficios_clave": ["Múltiples opciones para realizar los pagos del préstamo"]
    },
    {
        "pregunta": "¿Cómo se cuánto me falta pagar para finalizar el préstamo?",
        "respuesta": "En tu resumen de cuenta visualizarás el consumo realizado con la línea de crédito otorgada y el detalle de cuota en curso, tasa aplicada y monto de la cuota.",
        "tags": ["saldo_prestamo", "seguimiento_pago", "resumen_cuenta"],
        "keywords": ["cuánto falta pagar", "finalizar préstamo", "resumen de cuenta", "cuota en curso", "tasa aplicada"],
        "beneficios_clave": ["Claridad sobre el estado del préstamo y pagos restantes"]
    },
    {
        "pregunta": "¿Cuál es la diferencia entre crédito otorgado y disponible?",
        "respuesta": "El crédito otorgado es el límite que se te informa al momento de la solicitud. El crédito disponible es la diferencia entre el crédito otorgado y el utilizado, con este podrás seguir realizando consumos. Tené en cuenta que con cada utilización se realizará una nueva evaluación crediticia.",
        "tags": ["definicion_credito", "limite_credito", "disponible"],
        "keywords": ["crédito otorgado", "crédito disponible", "límite", "evaluación crediticia"],
        "beneficios_clave": ["Claridad en los conceptos de crédito otorgado y disponible"]
    },
    {
        "pregunta": "¿Dónde puedo ver el resumen de mi línea de crédito utilizada?",
        "respuesta": "Ingresando con tu usuario y contraseña en nuestra app o web podrás visualizar el detalle de tus consumos, el monto otorgado, el disponible, la fecha de vencimiento y los lugares de pago.",
        "tags": ["resumen_credito", "consulta_online", "gestion_credito"],
        "keywords": ["resumen línea de crédito", "consumos", "monto otorgado", "disponible", "fecha vencimiento", "lugares de pago"],
        "beneficios_clave": ["Acceso fácil al resumen de la línea de crédito", "Control de la información financiera"]
    },
    {
        "pregunta": "¿Qué es Efectivo en cuenta?",
        "respuesta": "Efectivo en cuenta es un préstamo para uso personal con acreditación en cuenta bancaria.",
        "tags": ["definicion_producto", "prestamo_personal", "acreditacion_bancaria"],
        "keywords": ["efectivo en cuenta", "préstamo personal", "acreditación bancaria"],
        "beneficios_clave": ["Acceso a préstamos personales con acreditación directa"]
    },
    {
        "pregunta": "¿Dónde puedo pedir mi Efectivo en cuenta?",
        "respuesta": "El préstamo podés solicitarlo a través de nuestra app web. El mismo está sujeto a evaluación crediticia.",
        "tags": ["solicitud_prestamo", "proceso_online", "evaluacion_crediticia"],
        "keywords": ["pedir efectivo en cuenta", "solicitar préstamo", "app web", "evaluación crediticia"],
        "beneficios_clave": ["Proceso de solicitud de préstamo online"]
    },
    {
        "pregunta": "¿Cómo se acredita el dinero del préstamo?",
        "respuesta": "Para la acreditación del préstamo, es necesario proporcionar un CBU de una cuenta en la que seas titular. El monto será acreditado en dicha cuenta en un plazo de hasta 96 horas hábiles.",
        "tags": ["acreditacion_prestamo", "CBU", "tiempos_acreditacion"],
        "keywords": ["acreditar préstamo", "CBU", "cuenta bancaria", "tiempo acreditación"],
        "beneficios_clave": ["Claridad sobre el proceso y tiempos de acreditación del préstamo"]
    },
    {
        "pregunta": "¿Afecta al disponible de mi Cencopay crédito?",
        "respuesta": "Este préstamo no afectará el disponible de tu tarjeta.",
        "tags": ["impacto_prestamo", "disponible_tarjeta", "financiamiento"],
        "keywords": ["afecta disponible", "préstamo", "tarjeta de crédito"],
        "beneficios_clave": ["El préstamo no reduce el disponible de la tarjeta de crédito"]
    },
    {
        "pregunta": "¿Cómo devuelvo el dinero?",
        "respuesta": "Las cuotas se debitarán en tu resumen de cuenta y las abonarás mediante el pago del mismo.",
        "tags": ["devolucion_prestamo", "pago_cuotas", "resumen_cuenta"],
        "keywords": ["devolver dinero", "pagar préstamo", "cuotas", "débito resumen"],
        "beneficios_clave": ["Proceso de devolución de préstamo integrado al resumen de cuenta"]
    },
    {
        "pregunta": "¿Tiene algún costo?",
        "respuesta": "Sí, este producto tiene un costo por la transferencia bancaria el cual vas a poder ver en www.cencopay.com.ar.",
        "tags": ["costos_prestamo", "transferencia_bancaria", "informacion_costos"],
        "keywords": ["costo préstamo", "transferencia bancaria", "comisiones"],
        "beneficios_clave": ["Transparencia sobre los costos asociados al préstamo"]
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