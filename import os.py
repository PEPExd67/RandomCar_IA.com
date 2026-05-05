import os
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
from dotenv import load_dotenv

# Cargar API KEY desde el .env
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Configuración del experto mecánico
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction="Eres el núcleo de RandomCar AI. Tu función es dar diagnósticos mecánicos precisos y técnicos. Responde de forma profesional sobre problemas automotrices."
)

# Ajustamos Flask para que busque el index.html en la carpeta raíz '.' 
# ya que en tu GitHub veo que no tienes carpeta 'templates'
app = Flask(__name__, template_folder='.')

@app.route('/')
def index():
    try:
        return render_template('index.html')
    except Exception as e:
        return f"Error: No se encontró index.html. Verifica la estructura en GitHub. {e}", 500

@app.route('/ask', methods=['POST'])
def ask():
    try:
        data = request.get_json()
        user_message = data.get("message")
        
        if not user_message:
            return jsonify({"response": "Proporcione datos de la falla."}), 400

        response = model.generate_content(user_message)
        return jsonify({"response": response.text})
    except Exception as e:
        return jsonify({"response": "Error de conexión con el núcleo central."}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
