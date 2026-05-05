import os
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
from dotenv import load_dotenv

# Cargar variables
load_dotenv()

# Configuración de la API de Google
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Usar el modelo gemini-1.5-flash directamente
model = genai.GenerativeModel("gemini-1.5-flash")

# --- EL CAMBIO ESTÁ AQUÍ ---
# Al no poner 'template_folder', Flask busca por defecto la carpeta 'templates'
app = Flask(__name__)

@app.route('/')
def index():
    try:
        return render_template('index.html')
    except Exception as e:
        # Si falla, nos dirá exactamente dónde buscó
        return f"Error: No se encontró index.html. Detalle: {e}", 500

@app.route('/ask', methods=['POST'])
def ask():
    try:
        data = request.get_json()
        user_message = data.get("message")
        
        if not user_message:
            return jsonify({"response": "Por favor, describe el problema."}), 400

        # Respuesta de la IA
        response = model.generate_content(user_message)
        
        return jsonify({"response": response.text})
    except Exception as e:
        return jsonify({"response": f"Error del sistema: {str(e)}"}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
