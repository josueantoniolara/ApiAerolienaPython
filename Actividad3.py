import folium
import requests
import json

def mostrar_mapa_meteorologico(latitud, longitud, api_key):
    """Muestra un mapa meteorológico con capas de OpenWeatherMap."""

    mapa = folium.Map(location=[latitud, longitud], zoom_start=7)

    # Capa de lluvia
    folium.TileLayer(
        tiles=f'http://tile.openweathermap.org/map/precipitation_new/{{z}}/{{x}}/{{y}}.png?appid={api_key}',
        attr='OpenWeatherMap',
        name='Lluvia',
        overlay=True,
        control=True
    ).add_to(mapa)

    # Capa de nubes
    folium.TileLayer(
        tiles=f'http://tile.openweathermap.org/map/clouds_new/{{z}}/{{x}}/{{y}}.png?appid={api_key}',
        attr='OpenWeatherMap',
        name='Nubes',
        overlay=True,
        control=True
    ).add_to(mapa)

    # Capa de temperatura
    folium.TileLayer(
        tiles=f'http://tile.openweathermap.org/map/temp_new/{{z}}/{{x}}/{{y}}.png?appid={api_key}',
        attr='OpenWeatherMap',
        name='Temperatura',
        overlay=True,
        control=True
    ).add_to(mapa)

    # Control de capas
    folium.LayerControl().add_to(mapa)

    return mapa

# Ejemplo de uso
latitud = 20.66682
longitud = -103.39215
api_key = "0fca9e7d1796d9188a59015215bac279"  # Reemplaza con tu clave de API

mapa_meteorologico = mostrar_mapa_meteorologico(latitud, longitud, api_key)
mapa_meteorologico.save("mapa_meteorologico.html")