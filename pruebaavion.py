from flask import Flask, render_template, request
import requests
import folium
import json

app = Flask(__name__)

API_KEY = "4a332c10643b7e1985a9d760f23a7045"  # Reemplaza con tu clave de API

def obtener_vuelos_con_ubicacion():
    """Obtiene todos los vuelos en vuelo con latitud y longitud."""
    url = f"http://api.aviationstack.com/v1/flights?access_key={API_KEY}&flight_status=active"

    try:
        response = requests.get(url)
        response.raise_for_status()
        datos = response.json()

        vuelos_con_ubicacion = []

        if datos.get("data"):
            for vuelo in datos["data"]:
                live_data = vuelo.get("live")
                if live_data and live_data.get("latitude") is not None and live_data.get("longitude") is not None:
                    vuelos_con_ubicacion.append({
                        "aerolinea": vuelo["airline"]["name"],
                        "numero_vuelo": vuelo["flight"]["number"],
                        "latitud": live_data["latitude"],
                        "longitud": live_data["longitude"]
                    })

        return vuelos_con_ubicacion

    except requests.exceptions.RequestException as e:
        print(f"Error de solicitud: {e}")
        return []
    except json.JSONDecodeError:
        print("Error al decodificar la respuesta JSON.")
        return []
    except KeyError:
        print("Error en la estructura de los datos recibidos.")
        return []

def generar_mapa_vuelo(numero_vuelo):
    """Genera un mapa con la ubicación de un vuelo específico."""
    url = f"http://api.aviationstack.com/v1/flights?access_key={API_KEY}&flight_number={numero_vuelo}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        datos = response.json()

        if datos["data"]:
            vuelo = datos["data"][0]
            live_data = vuelo.get("live")

            if live_data and live_data.get("latitude") is not None and live_data.get("longitude") is not None:
                latitud = live_data["latitude"]
                longitud = live_data["longitude"]
                aerolinea = vuelo["airline"]["name"]

                mapa = folium.Map(location=[latitud, longitud], zoom_start=7)

                folium.Marker(
                    location=[latitud, longitud],
                    popup=f"Aerolínea: {aerolinea}\nNúmero de vuelo: {numero_vuelo}",
                    icon=folium.Icon(color="red"),
                ).add_to(mapa)

                mapa.save("static/mapa_vuelo.html")
                return True

        return False  # No se encontró ubicación en tiempo real

    except requests.exceptions.RequestException as e:
        print(f"Error de solicitud: {e}")
        return False
    except json.JSONDecodeError:
        print("Error al decodificar la respuesta JSON.")
        return False
    except KeyError:
        print("Datos de vuelo no encontrados en la respuesta.")
        return False

@app.route("/", methods=["GET", "POST"])
def index():
    vuelos = obtener_vuelos_con_ubicacion()
    mapa_generado = False

    if request.method == "POST":
        numero_vuelo = request.form.get("numero_vuelo")
        if numero_vuelo:
            mapa_generado = generar_mapa_vuelo(numero_vuelo)

    return render_template("index.html", vuelos=vuelos, mapa_generado=mapa_generado)

if __name__ == "__main__":
    app.run(debug=True)
