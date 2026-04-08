import requests 
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://frascati.mx/campestre'
headers = {'User-Agent': 'Mozilla/5.0'}
respuesta = requests.get(url, headers=headers)
conteo = 0

datos_para_excel = []

productos_vistos = set() 

if respuesta.status_code == 200:
    soup = BeautifulSoup(respuesta.text, 'html.parser')
    tarjetas_productos = soup.find_all('div', class_='qrmenu-menu-items-content')

    for tarjeta in tarjetas_productos:
            
        titulo_html = tarjeta.find('div', class_='qrmenu-menu-items-title')
        categoria_html = tarjeta.find_previous('div', class_='qrmenu-category-header')
        precio_html = tarjeta.find('div', class_='qrmenu-menu-items-price')

        if titulo_html:
            span_problematico = titulo_html.find('span', class_='qrmenu-menu-items-label')
            if span_problematico:
                span_problematico.extract()
            
            titulo = titulo_html.get_text(strip=True)
        else:
            titulo = ""

        if titulo and (titulo not in productos_vistos):
            
            productos_vistos.add(titulo) 

            categoria = categoria_html.get_text(strip=True) if categoria_html else "Sin categoria"
            precio = precio_html.get_text(strip=True) if precio_html else "Sin precio"

            datos_para_excel.append({
                'PRODUCTO': titulo.upper(), 
                'CATEGORIA': categoria.upper(),
                'PRECIO': precio
            })
            
            conteo += 1
            
    print(f"{conteo} productos ÚNICOS encontrados.\n")
    
    df = pd.DataFrame(datos_para_excel)
    print(df)

    df.to_excel('menu_restaurante.xlsx', index=False)
    print("¡Éxito! Se ha creado el archivo 'menu_restaurante.xlsx'.")
    
else: 
    print(f'Error de conexión: {respuesta.status_code}')
