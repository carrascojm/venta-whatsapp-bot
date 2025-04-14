from fastapi import FastAPI, Form
from fastapi.responses import PlainTextResponse
from core_bot import (
    generar_respuesta_persuasiva,
    es_usuario_nuevo,
    guardar_en_historial,
    obtener_producto_activo
)
from twilio.rest import Client
import os
import threading
import uvicorn

app = FastAPI()

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_NUMBER = "whatsapp:+14155238886"  # Sandbox

twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

@app.post("/whatsapp")
async def whatsapp_webhook(
    From: str = Form(...),
    Body: str = Form(...)
):
    print(f"📩 Mensaje recibido de {From}: {Body}")

    def procesar():
        try:
            producto_info = obtener_producto_activo()
            if not producto_info:
                print("❌ No hay producto activo.")
                return
            nombre_producto = producto_info["nombre"]

            if es_usuario_nuevo(From):
                respuesta = (
                    "¡Hola! 👋 Bienvenido a nuestro canal de atención automática.\n\n"
                    "Soy tu asistente virtual y puedo contarte todo sobre nuestros productos y beneficios.\n"
                    f"Por ejemplo, tenemos un producto llamado {nombre_producto} con descuentos del 5% y más sorpresas.\n\n"
                    "Contame, ¿en qué puedo ayudarte hoy?"
                )
                guardar_en_historial(From, respuesta, tipo="bot", producto=nombre_producto)
            else:
                respuesta = generar_respuesta_persuasiva(usuario_id=From, mensaje_usuario=Body, producto=nombre_producto)

            print("🤖 Respuesta generada:", respuesta)

            twilio_client.messages.create(
                body=respuesta,
                from_=TWILIO_WHATSAPP_NUMBER,
                to=From
            )
        except Exception as e:
            print("❌ Error en procesamiento:", e)

    threading.Thread(target=procesar).start()
    return PlainTextResponse(status_code=200)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)