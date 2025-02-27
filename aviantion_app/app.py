from flask import Flask, render_template, request, jsonify
import requests
import json

app = Flask(__name__)

# Reemplaza 'YOUR_API_KEY' con tu clave API de AviationStack
API_KEY = '4a332c10643b7e1985a9d760f23a7045'
API_URL = 'http://api.aviationstack.com/v1/flights'

def get_flights(flight_iata=None):
    """Obtiene datos de vuelos de la API de AviationStack."""
    params = {
        'access_key': API_KEY,
        'flight_iata': flight_iata
    }
    try:
        response = requests.get(API_URL, params=params)
        response.raise_for_status()  # Lanza una excepción para códigos de estado HTTP erróneos
        data = response.json()
        return data.get('data', [])
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener datos de la API: {e}")
        return []

@app.route('/', methods=['GET', 'POST'])
def index():
    """Página principal que muestra todos los vuelos o resultados de búsqueda."""
    if request.method == 'POST':
        flight_iata = request.form.get('flight_iata')
        flights = get_flights(flight_iata)
        return render_template('results.html', flights=flights)
    else:
        flights = get_flights()
        return render_template('index.html', flights=flights)

if __name__ == '__main__':
    app.run(debug=True)