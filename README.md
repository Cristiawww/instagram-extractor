# 📸 Instagram Data Extractor

Proyecto de extracción de datos de cuentas públicas de Instagram usando la **API interna de Instagram** a través de la librería `Instaloader`.

> **Materia:** Dispositivos Móviles  
> **Restricciones:** Sin Selenium, sin BeautifulSoup  
> **Método:** API HTTP interna de Instagram (JSON)

---

## 🔧 Tecnologías utilizadas

| Herramienta | Uso |
|---|---|
| `Python 3.8+` | Lenguaje base |
| `Instaloader` | Librería que consume la API interna de Instagram vía HTTP |
| `json` | Guardar datos estructurados |
| `csv` | Exportar datos en formato tabular |

## ❓ ¿Por qué Instaloader?

Instaloader **no usa Selenium ni BeautifulSoup**. Funciona haciendo peticiones HTTP directas a los endpoints JSON internos de Instagram (e.g., `https://www.instagram.com/api/v1/users/web_profile_info/`), parsea las respuestas JSON y entrega los datos estructurados. Es equivalente a consumir una API REST.

---

## 🚀 Instalación

### 1. Clonar el repositorio
```bash
git clone https://github.com/TU_USUARIO/instagram-extractor.git
cd instagram-extractor
```

### 2. Crear entorno virtual (recomendado)
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

---

## ▶️ Uso

### Ejecución básica

```bash
python instagram_extractor.py
```

### Modificar el usuario a extraer

Edita esta línea en `instagram_extractor.py`:

```python
USERNAME = "instagram"   # ← Cambia esto al usuario que deseas
MAX_POSTS = 12           # ← Número de posts a extraer
```

### Usar como módulo en otro script

```python
from instagram_extractor import extraer_datos_perfil

datos = extraer_datos_perfil(username="nasa", max_posts=10)

# Acceder a datos del perfil
print(datos["perfil"]["seguidores"])
print(datos["perfil"]["biografia"])

# Acceder a publicaciones
for post in datos["publicaciones"]:
    print(post["url_post"], post["likes"])
```

---

## 📦 Datos extraídos

### Del perfil (`username_perfil.csv` + `username_datos.json`)
- `username`, `nombre_completo`, `biografia`
- `seguidores`, `seguidos`, `total_publicaciones`
- `es_verificado`, `es_privado`, `es_negocio`
- `categoria_negocio`, `url_foto_perfil`, `id_usuario`

### De las publicaciones (`username_posts.csv`)
- `shortcode`, `url_post`, `tipo` (imagen/video)
- `descripcion`, `likes`, `comentarios`, `visualizaciones`
- `fecha_publicacion`, `hashtags`, `menciones`, `ubicacion`

### Estadísticas calculadas
- Promedio de likes y comentarios
- Total acumulado de interacciones
- Número de posts extraídos

---

## 📁 Estructura del proyecto

```
instagram-extractor/
├── instagram_extractor.py   # Script principal
├── requirements.txt         # Dependencias
├── .gitignore               # Excluye datos y sesiones
└── README.md                # Este archivo
```

Los archivos de salida se guardan en `output_USERNAME/` (ignorado por Git).

---

## ⚠️ Notas importantes

- Solo funciona con **perfiles públicos** sin necesidad de login
- Para perfiles privados se requiere autenticación y ser seguidor
- Respetar los términos de servicio de Instagram
- No ejecutar demasiadas peticiones en poco tiempo para evitar bloqueos temporales

---

## 📄 Licencia

MIT License
