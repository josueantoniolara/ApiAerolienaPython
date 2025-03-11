import folium
import requests
import json

def mostrar_mapa_vuelos(api_key, numero_vuelo):
    """Muestra un mapa con la ubicación de un vuelo."""

    url = f"http://api.aviationstack.com/v1/flights?access_key={api_key}&flight_number={numero_vuelo}"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Lanza una excepción para códigos de error HTTP
        datos = response.json()

        if datos["data"]:
            vuelo = datos["data"][0]
            live_data = vuelo.get("live") #cambio aquí

            if live_data is not None:
                latitud = live_data["latitude"]
                longitud = live_data["longitude"]
                aerolinea = vuelo["airline"]["name"]

                mapa = folium.Map(location=[latitud, longitud], zoom_start=7)

                folium.Marker(
                    location=[latitud, longitud],
                    popup=f"Aerolínea: {aerolinea}\nNúmero de vuelo: {numero_vuelo}",
                    icon=folium.Icon(color="red"),
                ).add_to(mapa)

                return mapa
            else:
                print("No hay datos de ubicación en tiempo real para este vuelo.")
                return None
        else:
            print("No se encontraron datos para el vuelo.")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error de solicitud: {e}")
        return None
    except json.JSONDecodeError:
        print("Error al decodificar la respuesta JSON.")
        return None
    except KeyError:
        print("Datos de vuelo no encontrados en la respuesta.")
        return None

# Ejemplo de uso
api_key = "4a332c10643b7e1985a9d760f23a7045"  # Reemplaza con tu clave de API
numero_vuelo = "3863"  # Ejemplo de número de vuelo

mapa_vuelo = mostrar_mapa_vuelos(api_key, numero_vuelo)

if mapa_vuelo:
    mapa_vuelo.save("mapa_vuelo.html")