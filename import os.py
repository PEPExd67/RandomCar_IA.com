import os
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
from dotenv import load_dotenv

# 1. Cargar configuración
load_dotenv()

# 2. Configuración de Google Gemini con el nombre de modelo corregido
# Usamos 'models/gemini-1.5-flash' para evitar el error 404 v1beta
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

generation_config = {
    "temperature": 0.7,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 1000,
}

# Aquí está el cambio clave: 'models/gemini-1.5-flash'
model = genai.GenerativeModel(
    model_name="models/gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction="Eres RandomCar AI, un experto mecánico automotriz. Tu objetivo es ayudar a diagnosticar fallas de forma técnica y precisa."
)

# 3. Configuración de Flask (Carpeta estándar 'templates')
app = Flask(__name__, template_folder='templates')

@app.route('/')
def index():
    try:
        return render_template('index.html')
    except Exception as e:
        return f"Error: No se encontró index.html en la carpeta 'templates'. Detalle: {e}", 500

@app.route('/ask', methods=['POST'])
def ask():
    try:
        data = request.get_json()
        user_message = data.get("message")
        
        if not user_message:
            return jsonify({"response": "Por favor, describe el problema."}), 400

        # Iniciar chat y enviar mensaje
        chat_session = model.start_chat(history=[])
        response = chat_session.send_message(user_message)
        
        return jsonify({"response": response.text})
    
    except Exception as e:
        # Esto te mostrará el error real en la consola de Render si algo falla
        print(f"DEBUG ERROR: {e}")
        return jsonify({"response": f"Error del sistema: {str(e)}"}), 500

# 4. Lanzamiento para el servidor de Render
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
