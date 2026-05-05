import os
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
from dotenv import load_dotenv

# 1. CARGA DE CONFIGURACIÓN
load_dotenv()

# Configuración de la API de Google con manejo de errores
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    print("ERROR: No se encontró la GOOGLE_API_KEY en el archivo .env")
else:
    genai.configure(api_key=api_key)

# 2. INICIALIZACIÓN DEL MODELO
# Usamos 'models/gemini-1.5-flash-latest' para evitar el error 404 de versión
model = genai.GenerativeModel("models/gemini-1.5-flash-latest")

app = Flask(__name__)

# 3. RUTAS DE LA APLICACIÓN
@app.route('/')
def index():
    try:
        return render_template('index.html')
    except Exception as e:
        return f"Error: No se encontró index.html en la carpeta 'templates'. Detalle: {e}", 500

@app.route('/ask', methods=['POST'])
def ask():
    try:
        # Obtenemos los datos enviados desde el navegador
        data = request.get_json()
        user_message = data.get("message")
        
        if not user_message:
            return jsonify({"response": "Por favor, describe el problema del vehículo."}), 400

        # Instrucción interna para que la IA se comporte como un experto
        prompt_ingeniero = f"Eres un experto en mecánica automotriz. Analiza y responde brevemente a: {user_message}"

        # Generación de contenido con la IA
        response = model.generate_content(prompt_ingeniero)
        
        # Validación de respuesta segura
        if response.text:
            return jsonify({"response": response.text})
        else:
            return jsonify({"response": "El sistema no pudo generar un diagnóstico. Intenta ser más específico."})

    except Exception as e:
        print(f"Error en el servidor: {str(e)}")
        return jsonify({"response": f"Error del sistema: {str(e)}"}), 500

# 4. EJECUCIÓN DEL SERVIDOR
if __name__ == '__main__':
    # Render usa la variable PORT, si no existe usa el 5000 por defecto
    port = int(os.environ.get('PORT', 5000))
    print(f"Sistemas RandomCar AI iniciados en el puerto {port}")
    app.run(host='0.0.0.0', port=port)
