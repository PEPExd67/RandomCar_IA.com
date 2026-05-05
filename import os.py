import os
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
from dotenv import load_dotenv

# 1. Cargar variables de entorno
load_dotenv()

# 2. Configuración de Google Gemini
# Render leerá la clave desde la pestaña 'Environment'
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
    system_instruction="Eres RandomCar AI, un experto mecánico automotriz. Ayudas a los usuarios a diagnosticar fallas en sus vehículos basándote en ruidos, olores o comportamientos extraños de forma técnica y amigable."
)

# 3. Inicializar Flask
# Importante: Asegúrate de que tu carpeta se llame 'templates' en minúsculas
app = Flask(__name__, template_folder='templates')

@app.route('/')
def index():
    try:
        return render_template('index.html')
    except Exception as e:
        return f"Error: No se encontró index.html en la carpeta templates. {e}", 500

@app.route('/ask', methods=['POST'])
def ask():
    try:
        data = request.get_json()
        user_message = data.get("message")
        
        if not user_message:
            return jsonify({"response": "Escribe algo para poder ayudarte."}), 400

        chat_session = model.start_chat(history=[])
        response = chat_session.send_message(user_message)
        
        return jsonify({"response": response.text})
    
    except Exception as e:
        print(f"Error en el servidor: {e}")
        return jsonify({"response": "Lo siento, mi sistema de diagnóstico está fuera de línea. Intenta más tarde."}), 500

# 4. Configuración del puerto para Render
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
