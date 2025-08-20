from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from twilio.rest import Client
import os

app = FastAPI()

# Cargar variables de entorno
TWILIO_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER")

client = Client(TWILIO_SID, TWILIO_TOKEN)

class NotificacionRequest(BaseModel):
    nombres: str
    primer_apellido: str
    num_telefono: str

@app.post("/enviar-notificacion")
def enviar_notificacion(data: NotificacionRequest):
    try:
        mensaje = f"Hola {data.nombres} {data.primer_apellido}, tenemos una muy buena noticia para ti 😉"
        message = client.messages.create(
            body=mensaje,
            from_=TWILIO_WHATSAPP_NUMBER,
            to=f"whatsapp:+{data.num_telefono}"
        )
        return {"status": "enviado", "sid": message.sid}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
