import os
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
from dotenv import load_dotenv

# Cargar variables (útil para VS Code local)
load_dotenv()

# Configuración de Gemini
# Render leerá automáticamente la clave que pusiste en 'Environment'
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction="Eres RandomCar AI, un experto mecánico. Ayudas a diagnosticar fallas basándote en ruidos o síntomas de forma técnica."
)

# Inicializar Flask con la carpeta estándar 'templates'
app = Flask(__name__, template_folder='templates')

@app.route('/')
def index():
    try:
        # Flask buscará index.html dentro de la carpeta templates
        return render_template('index.html')
    except Exception as e:
        return f"Error: No se encontró index.html en la carpeta 'templates'. {str(e)}", 500

@app.route('/ask', methods=['POST'])
def ask():
    try:
        data = request.get_json()
        user_message = data.get("message")
        
        if not user_message:
            return jsonify({"response": "Por favor, describe el problema."}), 400

        chat = model.start_chat(history=[])
        response = chat.send_message(user_message)
        
        return jsonify({"response": response.text})
    except Exception as e:
        return jsonify({"response": f"Error del sistema: {str(e)}"}), 500

if __name__ == '__main__':
    # Usar el puerto que asigne Render o el 5000 por defecto
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
