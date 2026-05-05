import os
import google.generativeai as genai
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

# 1. Cargamos el archivo .env
load_dotenv()

# 2. Configuramos la API usando la variable de entorno
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

# 3. Configuración del modelo especializado
generation_config = {
    "temperature": 0.7,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 1000,
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction="Eres un experto maestro mecánico automotriz. Tu nombre es RandomCar AI. Respondes de forma profesional y técnica pero fácil de entender."
)

app = Flask(__name__)

# Rutas para tu sitio web
@app.route('/')
def index():
    # Flask buscará index.html automáticamente dentro de la carpeta 'templates'
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    try:
        user_message = request.json.get("message")
        if not user_message:
            return jsonify({"response": "No enviaste ningún mensaje."}), 400
            
        chat_session = model.start_chat(history=[])
        response = chat_session.send_message(user_message)
        
        return jsonify({"response": response.text})
    except Exception as e:
        return jsonify({"response": f"Error en el servidor: {str(e)}"}), 500

if __name__ == '__main__':
    # Render asigna un puerto dinámicamente, esto lo detecta
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
