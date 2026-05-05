import os
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
from dotenv import load_dotenv

# 1. Cargar variables
load_dotenv()

# 2. Configuración de Google Gemini corregida
# Aquí está el cambio clave para eliminar el error 404
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Configuramos el modelo de forma explícita
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash"
)

# 3. Inicializar Flask
app = Flask(__name__, template_folder='templates')

@app.route('/')
def index():
    try:
        return render_template('index.html')
    except Exception as e:
        return f"Error: No se encontró index.html. Detalle: {e}", 500

@app.route('/ask', methods=['POST'])
def ask():
    try:
        data = request.get_json()
        user_message = data.get("message")
        
        if not user_message:
            return jsonify({"response": "Escribe un problema para analizar."}), 400

        # Enviar mensaje a la IA
        response = model.generate_content(user_message)
        
        return jsonify({"response": response.text})
    
    except Exception as e:
        # Esto nos dirá exactamente qué pasa en los logs de Render
        print(f"Error detectado: {e}")
        return jsonify({"response": f"Error del sistema: {str(e)}"}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
