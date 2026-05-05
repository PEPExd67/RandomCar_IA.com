import os
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración de la API
# Render tomará la clave de la pestaña Environment que ya configuraste
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Configuración del modelo (Versión estable)
model = genai.GenerativeModel("gemini-1.5-flash")

app = Flask(__name__)

@app.route('/')
def home():
    # Flask buscará automáticamente en la carpeta 'templates' que ya creaste
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    try:
        data = request.get_json()
        mensaje_usuario = data.get("message")
        
        if not mensaje_usuario:
            return jsonify({"response": "Por favor, escribe algo."}), 400

        # Respuesta directa de la IA
        response = model.generate_content(mensaje_usuario)
        
        return jsonify({"response": response.text})
    
    except Exception as e:
        # Esto nos ayudará a ver qué pasa si algo falla
        print(f"Error en el servidor: {e}")
        return jsonify({"response": f"Hubo un problema técnico: {str(e)}"}), 500

if __name__ == '__main__':
    # Configuración para que funcione en el puerto de Render
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
