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

Instalación y configuración
Ver documentación de instalación para instrucciones detalladas sobre cómo configurar el bot en tu propio entorno.
Uso

Inicia una conversación con el bot en Telegram
Responde a las preguntas sobre tus intereses y preferencias
Recibe recomendaciones personalizadas de carreras disponibles en la UIP
Solicita más información sobre las carreras recomendadas si lo deseas
