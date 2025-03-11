from flask import Flask, render_template, request
import subprocess
import json

app = Flask(__name__)

API_KEY = "4a332c10643b7e1985a9d760f23a7045"

def obtener_vuelos_en_vuelo():
    """Obtiene vuelos en vuelo con todos los datos necesarios para la tabla."""
    url = f"http://api.aviationstack.com/v1/flights?access_key={API_KEY}&flight_status=active"

    try:
        resultado = subprocess.run(["curl", url], capture_output=True, text=True, check=True)
        datos = json.loads(resultado.stdout)

        vuelos_filtrados = []
        if datos.get("data"):
            for vuelo in datos["data"]:
                if vuelo["live"] is not None: # Verifica si hay datos en vivo
                    vuelos_filtrados.append({
                        "flight": vuelo["flight"],
                        "airline": vuelo["airline"],
                        "departure": vuelo["departure"],
                        "arrival": vuelo["arrival"],
                        "flight_status": vuelo["flight_status"],
                        "live": vuelo["live"]
                    })
        return vuelos_filtrados
    except subprocess.CalledProcessError as e:
        print(f"Error al obtener datos de la API: {e}")
        return []
    except json.JSONDecodeError:
        print("Error: Respuesta de la API inválida.")
        return []
    except KeyError:
        print("Error: Datos de vuelo no encontrados en la respuesta.")
        return []

@app.route("/", methods=["GET"])
def index():
    """Renderiza la página con los vuelos filtrados."""
    vuelos = obtener_vuelos_en_vuelo()
    busqueda = request.args.get("busqueda", "").lower()

    if busqueda:
        vuelos = [vuelo for vuelo in vuelos if busqueda in vuelo["airline"]["name"].lower() or busqueda in vuelo["flight"]["number"]]

    return render_template("index.html", vuelos=vuelos, busqueda=busqueda)

if __name__ == "__main__":
    app.run(debug=True)