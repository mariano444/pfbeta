from flask import Flask, request, render_template, jsonify
import subprocess
import os
import requests

app = Flask(__name__)

API_URL = "http://127.0.0.1:5000"  # Cambia la URL de la API según sea necesario

# Página principal con formulario
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        api_username = request.form.get("api_username")
        api_password = request.form.get("api_password")
        fb_username = request.form.get("fb_username")
        fb_password = request.form.get("fb_password")
        num_publications = int(request.form.get("num_publications"))

        # Validar credenciales de la API
        usos_restantes = validar_credenciales(api_username, api_password)
        if usos_restantes == 0:
            return jsonify({"message": "Credenciales incorrectas o límite de uso alcanzado"}), 403

        # Limitar la cantidad de publicaciones al máximo permitido
        num_publications = min(num_publications, usos_restantes)

        # Guardar los datos en un archivo temporal para que el script lo use
        with open("datos.txt", "w") as f:
            f.write(f"{fb_username},{fb_password},{num_publications}\n")

        # Ejecutar el script de manera local usando subprocess
        process = subprocess.Popen(["python", "script.py"])
        
        return jsonify({"message": "Script ejecutándose, las publicaciones se están realizando."}), 200

    return render_template("formulario.html")

def validar_credenciales(username, password):
    """Valida las credenciales usando la API proporcionada y devuelve el número máximo de publicaciones permitidas."""
    try:
        response = requests.post(f"{API_URL}/verificar_uso", json={"username": username, "password": password})

        if response.status_code == 200:
            data = response.json()
            print(f"Acceso permitido. Usos restantes: {data['uso_restante']}")
            return data['uso_restante']
        elif response.status_code == 403:
            print("Límite de uso alcanzado.")
            return 0
        elif response.status_code == 401:
            print("Credenciales incorrectas.")
            return 0
        else:
            print("Error desconocido al validar credenciales.")
            return 0
    except requests.exceptions.RequestException as e:
        print(f"Error al conectar con la API: {e}")
        return 0

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)

