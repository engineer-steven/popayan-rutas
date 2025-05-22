# Rutas en Popayán / Popayán Routes

## Descripción / Description

Este proyecto es una aplicación web que permite visualizar y calcular rutas en la ciudad de Popayán, Colombia. La aplicación utiliza un mapa interactivo donde los usuarios pueden seleccionar puntos de origen y destino para calcular la ruta óptima.


## Requisitos / Requirements

- Python 3.x
- Navegador web moderno / Modern web browser
- Conexión a internet / Internet connection
- Conda (Anaconda o Miniconda)

## Instalación / Installation

1. Clonar el repositorio / Clone the repository:
```bash
git clone []
cd Popayan-rutas
```

2. Crear y activar el entorno virtual 

Para Windows / For Windows:
```bash
# Crear el entorno virtual / Create virtual environment
conda create -n popayan-rutas python=3.x

# Activar el entorno virtual / Activate virtual environment
conda activate popayan-rutas
```

Para Linux/Mac / For Linux/Mac:
```bash
# Crear el entorno virtual / Create virtual environment
conda create -n popayan-rutas python=3.x

# Activar el entorno virtual / Activate virtual environment
source activate popayan-rutas
```

Nota: Una vez activado el entorno virtual, verás el nombre del entorno (popayan-rutas) al inicio de tu línea de comandos.

## Ejecución / Running the Application

El proyecto consta de dos partes: backend y frontend. Necesitas ejecutar ambos simultáneamente.

The project consists of two parts: backend and frontend. You need to run both simultaneously.

### Backend

1. Navegar al directorio del backend / Navigate to backend directory:
```bash
cd backend
```

2. Ejecutar el servidor backend / Run the backend server:
```bash
python app.py
```

### Frontend

1. En una nueva terminal, navegar al directorio del frontend / In a new terminal, navigate to frontend directory:
```bash
cd frontend
```

2. Iniciar el servidor web local / Start the local web server:
```bash
python -m http.server 8000
```

3. Abrir el navegador y visitar / Open your browser and visit:
```
http://localhost:8000
```

## Uso / Usage

1. En la interfaz web, verás un mapa de Popayán / In the web interface, you'll see a map of Popayán
2. Utiliza los menús desplegables para seleccionar el origen y destino / Use the dropdown menus to select origin and destination
3. Haz clic en "Calcular Ruta" para ver la ruta óptima / Click "Calcular Ruta" to see the optimal route

## Tecnologías Utilizadas / Technologies Used

- Frontend:
  - HTML5
  - CSS3
  - JavaScript
  - Leaflet.js (para mapas interactivos / for interactive maps)

- Backend:
  - Python
  - Flask (framework web / web framework)

## Contribución / Contributing

Las contribuciones son bienvenidas. Por favor, abre un issue para discutir los cambios propuestos.

Contributions are welcome. Please open an issue to discuss proposed changes.

