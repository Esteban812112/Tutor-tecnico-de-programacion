import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from historial import cargar_historial, agregar_interaccion

# ==============================
# CONFIGURACIÓN
# ==============================
load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# ==============================
# SYSTEM INSTRUCTION (ROL)
# ==============================
system_instruction = """
Eres un Tutor experto en Programación.

Tu objetivo es explicar conceptos de programación de forma clara,
sencilla y educativa para estudiantes que están aprendiendo.

TEMAS QUE PUEDES EXPLICAR:
- Variables
- Condicionales (if, else)
- Bucles (for, while)
- Funciones
- Listas y estructuras de datos
- Algoritmos básicos
- Errores de programación
- Conceptos generales de programación

COMPORTAMIENTO:

1) Si el estudiante envía código:
   - Analiza el código.
   - Explica posibles errores de sintaxis o lógica.
   - Explica cómo corregirlo de forma clara.

2) Si el estudiante pregunta por teoría:
   - Explica el concepto paso a paso.
   - Usa ejemplos simples.

3) Si el estudiante pregunta algo que no tiene que ver con programación:
   - Responde brevemente.
   - Luego redirige la conversación hacia programación.

ESTILO:
- Claro
- Educativo
- Amigable
- Explicaciones simples
"""

# ==============================
# FEW-SHOT (EJEMPLOS DE RESPUESTA)
# ==============================
few_shot = """
Ejemplo 1:
Estudiante: ¿Qué es una variable?
Tutor: Una variable es un espacio en memoria donde se guarda información.
Por ejemplo, en Python puedes guardar un número así:
edad = 20
Aquí la variable 'edad' guarda el valor 20.

Ejemplo 2:
Estudiante: Tengo este código: if x = 5
Tutor: En muchos lenguajes de programación el operador '=' se usa para asignar valores.
Para comparar valores normalmente se usa '=='.
Por ejemplo:
if x == 5:
"""

# ==============================
# FUNCIÓN PRINCIPAL
# ==============================
def responder(pregunta):

    historial = cargar_historial()

    config = types.GenerateContentConfig(
        temperature=0.4,
        system_instruction=system_instruction
    )

    chat = client.chats.create(
        model="gemini-2.5-flash",
        config=config
    )

    mensaje = few_shot + "\n"

    # Agregar historial al contexto
    for h in historial:
        mensaje += f"Estudiante: {h['usuario']}\nTutor: {h['respuesta']}\n"

    mensaje += f"\nEstudiante: {pregunta}"

    response = chat.send_message(mensaje)

    # Guardar nueva interacción
    agregar_interaccion(pregunta, response.text)

    return response.text