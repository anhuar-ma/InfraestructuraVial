# 🚧 InfraestructuraVial

## CRUD
Descripción: Aplicación de consola en **Python** que implementa un sistema **CRUD (Crear, Leer, Actualizar y Eliminar)** para la gestión de información relacionada con infraestructura vial, utilizando **Supabase** como backend.
---

### ⚙️ Requisitos previos

Antes de comenzar, asegúrate de tener instalado:

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

Puedes verificarlo con los siguientes comandos:

```bash
python --version
pip --version
```

### 📦 Instalación de dependencias

Para ejecutar el proyecto es necesario instalar las siguientes librerías:

```bash
pip install rich
pip install supabase
  ```


## 📊 DASHBOARD

Descripción: Aplicación web encargada de visualizar información almacenada en **Supabase**, permitiendo generar métricas, análisis y reportes en tiempo real para la toma de decisiones sobre la infraestructura vial.
El dashboard presenta los datos de manera clara mediante tablas, indicadores y gráficas interactivas.
---

### ⚙️ Requisitos previos

Antes de comenzar, asegúrate de contar con lo siguiente:

- 🔗 **URL del proyecto en Supabase**
- 🔑 **Clave pública (anon key) de Supabase**

Estas credenciales son necesarias para establecer la conexión entre la aplicación web y la base de datos.

---

### 🔐 Configuración básica

Debes agregar tus credenciales de Supabase en tu archivo JavaScript principal o en un archivo de configuración:

```bash
const SUPABASE_URL = "https://tu-proyecto.supabase.co";
const SUPABASE_ANON_KEY = "tu_api_key";
```
