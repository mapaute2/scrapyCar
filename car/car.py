import requests
from bs4 import BeautifulSoup
import pandas as pd

# Lista para almacenar los vehículos
vehiculos = []

# URLs para las páginas de 1 a 12
base_url = 'https://www.autotrader.com/cars-for-sale/hatchback?'
for pagina in range(0, 12):  # 0 a 11 para las 12 páginas
    first_record = pagina * 25  # Cada página muestra 25 vehículos
    url = f'{base_url}firstRecord={first_record}&newSearch=false'

    # Hacer la solicitud
    response = requests.get(url)

    if response.status_code == 200:
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')

        # Encontrar el elemento <h3> que contiene la información del vehículo
        for h3 in soup.find_all('h3', class_='text-bold text-size-400 link-unstyled'):
            texto = h3.text.strip()  # Ejemplo: '2024 Audi A5 2.0T Premium Plus'
            partes = texto.split(' ', 2)  # Separar el texto en partes
            if len(partes) >= 3:
                año = partes[0]  # '2024'
                marca = partes[1]  # 'Audi'
                modelo = partes[2]  # 'A5 2.0T Premium Plus'

                # Almacenar los datos en la lista
                vehiculos.append({
                    'año': año,
                    'marca': marca,
                    'modelo': modelo
                })

    else:
        print(f'Error al acceder a la página {pagina + 1}: {response.status_code}')

# Convertir a DataFrame y guardar como CSV
df = pd.DataFrame(vehiculos)
df.to_csv('vehiculos_autotrader.csv', index=False)

# Imprimir el número total de vehículos extraídos
print(f'Total de vehículos extraídos: {len(vehiculos)}')
