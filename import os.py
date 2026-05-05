import os
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
from dotenv import load_dotenv

# 1. Cargar variables de entorno (para desarrollo local)
load_dotenv()

# 2. Configuración de Google Gemini
# El código buscará la clave de forma segura en Render
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
    system_instruction="Eres un experto maestro mecánico automotriz llamado RandomCar AI. Ayudas a diagnosticar fallas basándote en descripciones de ruidos o síntomas de forma técnica pero fácil de entender."
)

app = Flask(__name__)

# 3. Rutas del sitio
@app.route('/')
def index():
    # Flask busca automáticamente dentro de la carpeta 'templates'
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    try:
        data = request.get_json()
        user_message = data.get("message")
        
        if not user_message:
            return jsonify({"response": "Por favor, escribe un mensaje."}), 400

        # Iniciar sesión de chat con el modelo
        chat_session = model.start_chat(history=[])
        response = chat_session.send_message(user_message)
        
        return jsonify({"response": response.text})
    
    except Exception as e:
        # Esto ayuda a ver errores en los logs de Render
        print(f"Error en el servidor: {e}")
        return jsonify({"response": "Hubo un problema al conectar con el experto mecánico."}), 500

# 4. Configuración del puerto para Render
if __name__ == '__main__':
    # Render asigna el puerto mediante una variable de entorno
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
