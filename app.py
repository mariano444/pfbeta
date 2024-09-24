import subprocess
import os
from flask import Flask, request, render_template, jsonify

app = Flask(__name__)

API_URL = "https://pf-ee7p.onrender.com/"

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        api_username = request.form.get("api_username")
        api_password = request.form.get("api_password")
        fb_username = request.form.get("fb_username")
        fb_password = request.form.get("fb_password")
        num_publications = int(request.form.get("num_publications"))

        usos_restantes = validar_credenciales(api_username, api_password)
        if usos_restantes == 0:
            return jsonify({"message": "Credenciales incorrectas o límite de uso alcanzado"}), 403

        num_publications = min(num_publications, usos_restantes)

        with open("datos.txt", "w") as f:
            f.write(f"{fb_username},{fb_password},{num_publications}\n")

        # Ejecutar el script con configuración headless
        process = subprocess.Popen(
            ["python", "script.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        stdout, stderr = process.communicate()

        if process.returncode != 0:
            return jsonify({"message": "Error al ejecutar el script", "error": stderr}), 500

        return jsonify({"message": "Script ejecutándose, las publicaciones se están realizando."}), 200

    return render_template("formulario.html")

def validar_credenciales(username, password):
    try:
        response = requests.post(f"{API_URL}/verificar_uso", json={"username": username, "password": password})

        if response.status_code == 200:
            data = response.json()
            return data['uso_restante']
        return 0
    except requests.exceptions.RequestException as e:
        return 0

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
