# Popayán Rutas

Este proyecto es una aplicación web para encontrar rutas en la ciudad de Popayán, Colombia. Utiliza un grafo de la red vial de la ciudad para calcular las rutas más cortas entre diferentes puntos de interés.

## Características

- Cálculo de rutas entre puntos de interés en Popayán
- Visualización de rutas en un mapa interactivo
- Interfaz web moderna y fácil de usar
- Backend en Python con Flask
- Frontend con React

## Requisitos

- Python 3.8+
- Node.js 14+
- npm o yarn

## Instalación

### Backend

```bash
cd backend
pip install -r requirements.txt
python app.py
```

### Frontend

```bash
cd frontend
npm install
npm start
```

## Estructura del Proyecto

- `/backend`: Servidor Flask con la lógica de cálculo de rutas
- `/frontend`: Aplicación React para la interfaz de usuario
- `/utils`: Utilidades y funciones auxiliares

## Tecnologías Utilizadas

- Backend:
  - Flask
  - NetworkX
  - Shapely
  - Flask-CORS

- Frontend:
  - React
  - Leaflet
  - Material-UI

## Licencia

MIT 