import os
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
from dotenv import load_dotenv

# 1. Cargar variables de entorno para seguridad
load_dotenv()

# 2. Configuración de la IA (Gemini)
# Render buscará 'GOOGLE_API_KEY' en la pestaña Environment
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

generation_config = {
    "temperature": 0.7,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 1000,
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction="Eres RandomCar AI, un experto mecánico automotriz. Tu objetivo es ayudar a diagnosticar fallas de forma técnica y precisa."
)

# 3. Configuración de Flask
# Usamos el nombre estándar 'templates' para evitar errores de ruta
app = Flask(__name__, template_folder='templates')

@app.route('/')
def index():
    try:
        return render_template('index.html')
    except Exception as e:
        # Este mensaje te avisará si la carpeta o el archivo están mal puestos
        return f"Error Crítico: No se encontró 'index.html' dentro de la carpeta 'templates'. Detalle: {e}", 500

@app.route('/ask', methods=['POST'])
def ask():
    try:
        data = request.get_json()
        user_message = data.get("message")
        
        if not user_message:
            return jsonify({"response": "Por favor, describe el problema de tu auto."}), 400

        # Iniciar chat con la IA
        chat_session = model.start_chat(history=[])
        response = chat_session.send_message(user_message)
        
        return jsonify({"response": response.text})
    
    except Exception as e:
        print(f"Error en el servidor: {e}")
        return jsonify({"response": "Lo siento, el sistema de diagnóstico está en mantenimiento."}), 500

# 4. Lanzamiento para Render
if __name__ == '__main__':
    # Render asigna el puerto dinámicamente
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
