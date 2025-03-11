import subprocess
import json

def obtener_vuelos_en_vuelo(api_key):
    """Obtiene datos de vuelos en vuelo usando AviationStack."""

    url = f"http://api.aviationstack.com/v1/flights?access_key={api_key}&flight_status=active"

    try:
        resultado = subprocess.run(["curl", url], capture_output=True, text=True, check=True)
        datos = json.loads(resultado.stdout)

        if datos["data"]:
            for vuelo in datos["data"]:
                aerolinea = vuelo["airline"]["name"]
                numero_vuelo = vuelo["flight"]["number"]
                ubicacion = vuelo["live"]
                if ubicacion is not None:
                  latitud = ubicacion["latitude"]
                  longitud = ubicacion["longitude"]
                  print(f"Aerolínea: {aerolinea}, Número de vuelo: {numero_vuelo}, Latitud: {latitud}, Longitud: {longitud}")
                else:
                  print(f"Aerolínea: {aerolinea}, Número de vuelo: {numero_vuelo}, Ubicación no disponible")
        else:
            print("No se encontraron vuelos en vuelo.")

    except subprocess.CalledProcessError as e:
        print(f"Error: No se pudieron obtener los datos de los vuelos. {e}")
    except json.JSONDecodeError:
        print("Error: Respuesta de la API inválida.")
    except KeyError:
        print("Error: Datos de vuelo no encontrados en la respuesta.")

# Ejemplo de uso
api_key = "4a332c10643b7e1985a9d760f23a7045"  # Reemplaza con tu clave de API

obtener_vuelos_en_vuelo(api_key)