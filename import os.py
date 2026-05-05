import os
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Configuración de la API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Intentamos con el nombre de modelo más específico
# Si este falla, prueba cambiando a "gemini-1.5-pro" solo para testear
MODEL_NAME = "gemini-1.5-flash-latest" 

model = genai.GenerativeModel(model_name=MODEL_NAME)

app = Flask(__name__, template_folder='templates')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    try:
        data = request.get_json()
        mensaje = data.get("message")
        
        # Usamos la función más básica de generación
        response = model.generate_content(mensaje)
        
        if response.text:
            return jsonify({"response": response.text})
        else:
            return jsonify({"response": "La IA no devolvió texto. Revisa tu cuota en Google AI Studio."})
            
    except Exception as e:
        print(f"ERROR DETECTADO: {str(e)}")
        # Si sigue dando 404, este mensaje te lo confirmará en la pantalla
        return jsonify({"response": f"Error del motor (404): {str(e)}. Intenta cambiar el nombre del modelo en el código."}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
