# HojaldreBot

Miguel: Asistente de Orientación Vocacional para la UIP
Descripción
Miguel es un asistente de orientación vocacional basado en inteligencia artificial, diseñado específicamente para ayudar a estudiantes a encontrar la carrera ideal en la Universidad Interamericana de Panamá (UIP). Utilizando un bot de Telegram como interfaz de usuario, Miguel realiza una serie de preguntas personalizadas para comprender los intereses, habilidades y aspiraciones de los estudiantes, y recomienda entre 1 y 3 carreras disponibles en la UIP que mejor se adapten a su perfil.
Características

Interfaz conversacional: Interactúa con los usuarios a través de Telegram, proporcionando una experiencia accesible desde cualquier dispositivo móvil.
Recomendaciones personalizadas: Ofrece sugerencias de carreras basadas en múltiples factores, incluyendo intereses personales, fortalezas académicas y objetivos profesionales.
Base de datos actualizada: Contiene exclusivamente carreras oficiales ofrecidas por la UIP, organizadas en 5 categorías principales.
Memoria conversacional: Mantiene el contexto de la conversación para proporcionar recomendaciones más precisas.
Explicaciones claras: Complementa cada recomendación con una breve explicación de por qué esa carrera podría ser adecuada para el usuario.

Tecnologías utilizadas

AWS Lambda: Para la ejecución serverless del código.
Amazon DynamoDB: Para almacenar y mantener el historial de conversaciones.
OpenAI API: Motor de procesamiento de lenguaje natural para interpretar las respuestas de los usuarios.
Telegram Bot API: Para la interfaz de usuario.
Python: Lenguaje de programación principal.

Categorías de carreras disponibles

🧠 Ciencias de la Salud
📊 Ciencias Administrativas, Marítima y Portuaria
🛠 Ingeniería, Arquitectura y Diseño
🏨 Hotelería, Gastronomía y Turismo
⚖️ Derecho y Ciencias Políticas

Arquitectura
El sistema se compone de tres componentes principales:

Bot de Telegram: Interfaz para la interacción con el usuario.
Función Lambda: Procesa los mensajes y genera respuestas utilizando la API de OpenAI.
Base de datos DynamoDB: Almacena las conversaciones para mantener el contexto.

Instrucciones para ejecutar el proyecto
Prerrequisitos

Python 3.8 o superior
pip (administrador de paquetes de Python)
Cuenta en Telegram
Cuenta en AWS con acceso a Lambda, DynamoDB y API Gateway
Cuenta en OpenAI con acceso a la API

Pasos para configuración

Crear un bot de Telegram

Habla con @BotFather en Telegram
Sigue las instrucciones para crear un nuevo bot
Guarda el token proporcionado


Crear capa Lambda con dependencias
bash# Crear directorio para la capa
mkdir -p layer/python

# Instalar las dependencias necesarias
pip install openai==0.28.1 boto3 urllib3 requests -t layer/python

# Crear el archivo ZIP para la capa
cd layer
zip -r ../layer.zip python/


Configuración en AWS
DynamoDB

Crear tabla DynamoDB

Nombre de la tabla: miguel-conversations (o el que prefieras)
Clave de partición: chat_id (String)
Configuración de capacidad: Bajo demanda



Lambda

Crear función Lambda

Runtime: Python 3.9
Arquitectura: x86_64
Memoria: 256 MB
Timeout: 45 segundos
Almacenamiento efímero: 512 MB


Subir código

Zip el código fuente: zip -r lambda_function.zip lambda_function.py
Sube este archivo ZIP a Lambda
Adjunta la capa creada anteriormente


Configurar variables de entorno en Lambda

OPENAI_API_KEY: Tu clave API de OpenAI
TELEGRAM_BOT_TOKEN: Token de tu bot de Telegram
DYNAMODB_TABLE_NAME: Nombre de tu tabla DynamoDB


Configurar permisos

Asegúrate de que el rol de ejecución de Lambda tenga permisos para acceder a DynamoDB
Política recomendada: AmazonDynamoDBFullAccess (o una más restrictiva para producción)



API Gateway

Crear API REST

Crear un nuevo recurso (por ejemplo, /webhook)
Crear método POST


Configurar integración con Lambda

Tipo: Lambda Function
Lambda Function: Selecciona la función creada anteriormente
Usar Lambda Proxy integration: Sí


Desplegar API

Crear nueva etapa (por ejemplo, prod)
Desplegar la API
Copiar la URL del endpoint


Configurar webhook de Telegram
bashcurl -F "url=https://tu-api-gateway-url.amazonaws.com/prod/webhook" https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/setWebhook


Uso del bot

Inicia una conversación con el bot en Telegram
Responde a las preguntas sobre tus intereses y preferencias
Recibe recomendaciones personalizadas de carreras disponibles en la UIP
Solicita más información sobre las carreras recomendadas si lo deseas

Contenido del repositorio

lambda_function.py: Código principal del asistente
README.md: Este archivo
Documentación técnica: Detalles técnicos completos del proyecto
Diagrama de flujo: Representación visual del proceso del chat

Licencia
Este proyecto es para fines educativos como parte del curso de Programación V en la Universidad Interamericana de Panamá.
