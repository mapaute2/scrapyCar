from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

# Configura el controlador de Selenium
driver = webdriver.Chrome()  # Asegúrate de tener ChromeDriver en tu PATH

# Lista para almacenar los vehículos
vehiculos = []

# URL base para la búsqueda de hatchbacks
base_url = 'https://www.autotrader.com/cars-for-sale/hatchback?'

# Iterar sobre las páginas
for pagina in range(0, 12):  # 0 a 11 para las 12 páginas
    first_record = pagina * 25  # Cada página muestra 25 vehículos
    url = f'{base_url}firstRecord={first_record}&newSearch=false'

    # Abrir la URL
    driver.get(url)

    try:
        # Esperar a que los elementos de vehículos estén visibles
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'text-bold.text-size-400.link-unstyled'))
        )

        # Encontrar el elemento <h3> que contiene la información del vehículo
        h3_elements = driver.find_elements(By.CLASS_NAME, 'text-bold.text-size-400.link-unstyled')

        for h3 in h3_elements:
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

    except Exception as e:
        print(f"Error al cargar la página {pagina + 1}: {str(e)}")

# Cerrar el navegador
driver.quit()

# Convertir a DataFrame y guardar como CSV
df = pd.DataFrame(vehiculos)
df.to_csv('vehiculos_autotrader.csv', index=False)

# Imprimir el número total de vehículos extraídos
print(f'Total de vehículos extraídos: {len(vehiculos)}')
