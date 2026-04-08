# 📄 Scraper de menú de restaurante (Frascati)

## 🧾 Descripción

Este script en Python realiza **web scraping** sobre el sitio del menú de un restaurante, extrae información de los productos (nombre, categoría y precio), elimina duplicados y guarda los resultados en un archivo de Excel.

---

## ⚙️ Tecnologías utilizadas

* `requests` → Para realizar la petición HTTP
* `BeautifulSoup` (`bs4`) → Para parsear el HTML
* `pandas` → Para estructurar los datos y exportarlos a Excel

---

## 🌐 URL objetivo

```
https://frascati.mx/campestre
```

---

## 🔍 Funcionamiento paso a paso

### 1. Importación de librerías

```python
import requests
from bs4 import BeautifulSoup
import pandas as pd
```

---

### 2. Configuración de la petición

```python
url = 'https://frascati.mx/campestre'
headers = {'User-Agent': 'Mozilla/5.0'}
respuesta = requests.get(url, headers=headers)
```

Se define la URL y un `User-Agent` para simular un navegador real.

---

### 3. Inicialización de variables

```python
conteo = 0
datos_para_excel = []
productos_vistos = set()
```

* `conteo`: lleva el número de productos únicos
* `datos_para_excel`: almacena los datos extraídos
* `productos_vistos`: evita duplicados

---

### 4. Verificación de respuesta

```python
if respuesta.status_code == 200:
```

Se asegura que la petición fue exitosa.

---

### 5. Parseo del HTML

```python
soup = BeautifulSoup(respuesta.text, 'html.parser')
tarjetas_productos = soup.find_all('div', class_='qrmenu-menu-items-content')
```

Se buscan las tarjetas de productos dentro del HTML.

---

### 6. Extracción de datos

Para cada producto:

```python
titulo_html = tarjeta.find('div', class_='qrmenu-menu-items-title')
categoria_html = tarjeta.find_previous('div', class_='qrmenu-category-header')
precio_html = tarjeta.find('div', class_='qrmenu-menu-items-price')
```

---

### 7. Limpieza del título

Se elimina un `span` no deseado dentro del título:

```python
span_problematico = titulo_html.find('span', class_='qrmenu-menu-items-label')
if span_problematico:
    span_problematico.extract()
```

---

### 8. Filtrado de duplicados

```python
if titulo and (titulo not in productos_vistos):
    productos_vistos.add(titulo)
```

Evita guardar productos repetidos.

---

### 9. Estructuración de datos

```python
datos_para_excel.append({
    'PRODUCTO': titulo.upper(),
    'CATEGORIA': categoria.upper(),
    'PRECIO': precio
})
```

Convierte texto a mayúsculas para consistencia.

---

### 10. Creación del DataFrame

```python
df = pd.DataFrame(datos_para_excel)
print(df)
```

---

### 11. Exportación a Excel

```python
df.to_excel('menu_restaurante.xlsx', index=False)
```

Se genera el archivo:

```
menu_restaurante.xlsx
```

---

### 12. Manejo de errores

```python
else: 
    print(f'Error de conexión: {respuesta.status_code}')
```

---

## 📊 Resultado

* Archivo Excel con columnas:

  * PRODUCTO
  * CATEGORIA
  * PRECIO
* Solo productos únicos
* Datos limpios y estructurados

---

## ⚠️ Posibles mejoras

* Manejo de errores más robusto (`try/except`)
* Uso de `logging` en lugar de `print`
* Soporte para cambios en la estructura HTML
* Exportar también a CSV o base de datos
* Agregar timestamps

---

## 🚀 Ejecución

```bash
python script.py
```
