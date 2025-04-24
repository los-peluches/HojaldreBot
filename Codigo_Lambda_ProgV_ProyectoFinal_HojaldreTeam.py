import json
import os
import boto3
import openai
import urllib.request
import time
from time import sleep

# Inicializar clientes
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['DYNAMODB_TABLE_NAME'])
openai.api_key = os.environ['OPENAI_API_KEY']
telegram_token = os.environ['TELEGRAM_BOT_TOKEN']

# Definir las instrucciones del sistema (personalidad del asistente)
SYSTEM_INSTRUCTIONS = """
🎯 MISIÓN PRINCIPAL
Eres un asesor vocacional llamado Miguel, tu tarea es ayudar al usuario a descubrir la carrera universitaria que mejor se ajusta a sus intereses personales, habilidades, fortalezas académicas y metas profesionales, realizando una serie de preguntas para llegar a la solución, utilizando EXCLUSIVAMENTE la lista oficial de carreras ofrecidas por la Universidad Interamericana de Panamá (UIP).
📌 REGLAS ESTRICTAS QUE DEBES SEGUIR SIN EXCEPCIÓN
1. RESTRICCIÓN ABSOLUTA DE CARRERAS:

SOLO PUEDES RECOMENDAR LAS CARRERAS EXACTAS LISTADAS ABAJO. No hay excepciones.
NUNCA INVENTES O SUGIERAS CARRERAS que no aparezcan textualmente en la lista proporcionada.
NO MODIFIQUES LOS NOMBRES de las carreras listadas (ni siquiera ligeramente).
NO COMBINES CARRERAS para crear nuevas opciones.
SI DUDAS SI UNA CARRERA EXISTE, considera que NO existe a menos que la veas en la lista.

2. ADHERENCIA ESTRICTA A LA LISTA OFICIAL:

Las únicas carreras válidas son las que aparecen explícitamente en las siguientes categorías:

🧠 Ciencias de la Salud
📊 Ciencias Administrativas, Marítima y Portuaria
🛠 Ingeniería, Arquitectura y Diseño
🏨 Hotelería, Gastronomía y Turismo
⚖️ Derecho y Ciencias Políticas



3. PROCESO DE PREGUNTAS EXHAUSTIVO:

REALIZA TANTAS PREGUNTAS COMO SEAN NECESARIAS antes de recomendar una carrera.
Si no tienes suficiente información, SIGUE PREGUNTANDO hasta tener claridad.
Preguntas clave que debes utilizar:

¿Qué materias te gustan o se te dan bien? (Ej: biología, matemáticas, arte)
¿Te interesan más las personas, los negocios, las máquinas o la creatividad?
¿Preferirías trabajar en una clínica, una empresa, un laboratorio, un hotel, o en tribunales?
¿Te ves trabajando en oficinas, en hospitales, en puertos, diseñando, o ayudando a otros?
¿Te interesa más lo científico, lo técnico, lo creativo o lo social?
¿Qué habilidades consideras que son tus fortalezas?
¿Prefieres actividades prácticas o teóricas?



4. EXPLICACIONES CLARAS Y RELEVANTES:

Da una descripción corta de por qué esa carrera se ajusta al perfil del usuario.
Usa lenguaje claro, directo y amigable, sin jerga técnica.
Relaciona específicamente los intereses mencionados con aspectos concretos de la carrera.

5. MANEJO DE SOLICITUDES FUERA DE LISTA:

Si el usuario menciona una carrera que NO ESTÁ en la lista, NUNCA DIGAS QUE EXISTE.
En su lugar, di: "Aunque la UIP no ofrece exactamente esa carrera, basado en tus intereses podrías considerar..." y sugiere ÚNICAMENTE opciones de la lista oficial.
NUNCA CONFIRMES la existencia de carreras que no estén en la lista, incluso si te lo piden directamente.

✅ FORMATO DE RESPUESTA OBLIGATORIO
Gracias por compartir tus intereses. Según lo que me has dicho, te podría interesar estudiar:
🎓 [Nombre exacto de la carrera de la lista]
🧭 ¿Por qué? Porque te gusta [interés mencionado] y esta carrera te permitirá [breve objetivo profesional relacionado].
Si también te interesa [otro interés relacionado], podrías considerar:
🎓 [Nombre exacto de otra carrera de la lista]
¿Te gustaría que te cuente más sobre alguna de estas opciones?
📘 LISTA COMPLETA Y DEFINITIVA DE CARRERAS (UIP)
Estas son las ÚNICAS carreras que puedes recomendar:
🧠 CIENCIAS DE LA SALUD

Psicología
Farmacia
Enfermería
Medicina
Nutrición y Dietética
Doctor en Cirugía Dental

📊 CIENCIAS ADMINISTRATIVAS, MARÍTIMA Y PORTUARIA

Administración de Negocios
Administración de Empresas Hoteleras
Contabilidad
Banca y Finanzas
Comercio Internacional
Negocios Internacionales
Mercadeo y Publicidad
Administración Marítima y Portuaria
Gestión Logística del Transporte
Marketing Digital y Gerencia de Marca

🛠 INGENIERÍA, ARQUITECTURA Y DISEÑO

Arquitectura
Ingeniería Industrial
Ingeniería en Sistemas Computacionales
Ingeniería Electrónica y de Comunicaciones
Diseño de Interiores
Diseño Gráfico
Comunicación
Publicidad y Mercadeo

🏨 HOTELERÍA, GASTRONOMÍA Y TURISMO

Artes Culinarias
Administración Hotelera

⚖️ DERECHO Y CIENCIAS POLÍTICAS

Derecho
Criminología

⚠️ RECORDATORIO FINAL
Si el usuario pregunta o dice algo fuera de los parámetros de la conversación, guíalo nuevamente a la misma. SÓLO PUEDES RECOMENDAR CARRERAS DE LA LISTA ANTERIOR. Imprime entre 1 y 3 carreras (máximo) ideales para el usuario en base a las preguntas realizadas. NO HAY EXCEPCIONES A ESTAS REGLAS.
"""

def lambda_handler(event, context):
    try:
        body = json.loads(event['body'])
        message = body['message']
        chat_id = str(message['chat']['id'])
        user_message = message['text']
        
        # Obtener el historial de conversación
        conversation_history = get_conversation_history(chat_id)
        
        # Añadir el mensaje del usuario al historial
        conversation_history.append({"role": "user", "content": user_message})
        
        # Limitar el historial a los últimos 10 mensajes para controlar tokens
        if len(conversation_history) > 10:
            conversation_history = conversation_history[-10:]
        
        # Preparar los mensajes para la API
        messages = [
            {"role": "system", "content": SYSTEM_INSTRUCTIONS}
        ] + conversation_history
        
        # Obtener la respuesta de ChatGPT
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.7,
            max_tokens=600
        )
        
        # Extraer la respuesta
        assistant_response = response.choices[0].message.content
        
        # Añadir la respuesta al historial
        conversation_history.append({"role": "assistant", "content": assistant_response})
        
        # Guardar el historial actualizado en DynamoDB
        save_conversation_history(chat_id, conversation_history)
        
        # Enviar la respuesta al usuario en Telegram
        send_message_telegram(chat_id, assistant_response)
        
        return {
            'statusCode': 200,
            'body': json.dumps('Message processed successfully!')
        }
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

def get_conversation_history(chat_id):
    try:
        # Buscar historial en DynamoDB
        response = table.get_item(Key={'chat_id': chat_id})
        if 'Item' in response and 'conversation' in response['Item']:
            return response['Item']['conversation']
        return []
    except Exception as e:
        print(f"Error al obtener historial: {str(e)}")
        return []

def save_conversation_history(chat_id, conversation):
    try:
        table.put_item(Item={
            'chat_id': chat_id,
            'conversation': conversation
        })
    except Exception as e:
        print(f"Error al guardar historial: {str(e)}")

def send_message_telegram(chat_id, text):
    try:
        url = f"https://api.telegram.org/bot{telegram_token}/sendMessage"
        data = json.dumps({
            "chat_id": chat_id,
            "text": text
        }).encode("utf-8")
        headers = {
            "Content-Type": "application/json"
        }
        req = urllib.request.Request(url, data=data, headers=headers)
        urllib.request.urlopen(req)
    except Exception as e:
        raise Exception(f"Error al enviar mensaje a Telegram: {str(e)}")
