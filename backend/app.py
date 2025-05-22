from flask import Flask, request, jsonify
from flask_cors import CORS
import networkx as nx
from utils import encontrar_nodo_mas_cercano, encontrar_nodo_destino_correcto
import shapely.wkt

app = Flask(__name__)
CORS(app)

# Cargar el grafo desde archivo
print("Cargando grafo de Popayán desde archivo...")
G = nx.read_graphml("popayan.graphml")
print(f"Nodos: {len(G.nodes)}, Aristas: {len(G.edges)}")

# Asegurar que el grafo es dirigido
if not nx.is_directed(G):
    G = G.to_directed()

# Convertir el atributo 'length' de todas las aristas a float
for u, v, k, data in G.edges(keys=True, data=True):
    if 'length' in data:
        data['length'] = float(data['length'])

# Definir lugares importantes en Popayán (coordenadas originales)
lugares_importantes = {
    "Terminal": [2.450481, -76.609428],
    "Universidad del Cauca": [2.440829, -76.604511],
    "Parque Caldas": [2.442499, -76.606542],
    "Hospital San José":[2.449296, -76.600833],
    "Centro Comercial Campanario": [2.460268, -76.595910],
    "Aeropuerto": [2.451773, -76.609893],
    "Mercado La Esmeralda": [2.444843, -76.615153],  
    "Iglesia San Francisco": [2.443128, -76.608357],
    "unicomfacauca": [2.442974, -76.607986],
    "colegio unicomfa": [2.443486, -76.606822]
}
lugares_nodos = {}
lugares_nodos_coords = {}
for nombre, coords in lugares_importantes.items():
    nodo, _ = encontrar_nodo_mas_cercano(G, float(coords[0]), float(coords[1]), modo='origen')
    lugares_nodos[nombre] = nodo
    punto = G.nodes[nodo]
    lugares_nodos_coords[nombre] = [float(punto['y']), float(punto['x'])]

@app.route('/lugares', methods=['GET'])
def obtener_lugares():
    # Devolver las coordenadas originales definidas por el usuario
    return jsonify(lugares_importantes)

@app.route('/ruta', methods=['POST'])
def ruta():
    try:
        data = request.get_json()
        origen_nombre = data['origen_nombre']
        destino_nombre = data['destino_nombre']
        origen_nodo = lugares_nodos[origen_nombre]
        destino_nodo = lugares_nodos[destino_nombre]
        origen_coords = lugares_importantes[origen_nombre]
        destino_coords = lugares_importantes[destino_nombre]
        # Buscar nodo de origen y destino más cercanos accesibles
        origen_nodo, _ = encontrar_nodo_mas_cercano(G, float(origen_coords[0]), float(origen_coords[1]), modo='origen')
        destino_nodo, _ = encontrar_nodo_mas_cercano(G, float(destino_coords[0]), float(destino_coords[1]), modo='origen')
        ruta_nodos = nx.shortest_path(G, origen_nodo, destino_nodo, weight='length')
        ruta_coords = []
        # Siempre agrega el punto de origen como primer punto de la ruta
        ruta_coords.append([float(origen_coords[0]), float(origen_coords[1])])
        primer_nodo = G.nodes[ruta_nodos[0]]
        segundo_nodo = G.nodes[ruta_nodos[1]] if len(ruta_nodos) > 1 else None
        dist_primer = ((float(primer_nodo['y']) - float(origen_coords[0]))**2 + (float(primer_nodo['x']) - float(origen_coords[1]))**2) ** 0.5
        dist_segundo = ((float(segundo_nodo['y']) - float(origen_coords[0]))**2 + (float(segundo_nodo['x']) - float(origen_coords[1]))**2) ** 0.5 if segundo_nodo else None
        if segundo_nodo and dist_segundo < dist_primer:
            ruta_coords.append([float(segundo_nodo['y']), float(segundo_nodo['x'])])
            start_index = 1
        else:
            if [float(origen_coords[0]), float(origen_coords[1])] != [float(primer_nodo['y']), float(primer_nodo['x'])]:
                ruta_coords.append([float(primer_nodo['y']), float(primer_nodo['x'])])
            start_index = 0
        # Recorrer la ruta sobre la red vial desde el nodo útil
        for i in range(start_index, len(ruta_nodos) - 1):
            u = ruta_nodos[i]
            v = ruta_nodos[i + 1]
            edge_data = G.get_edge_data(u, v)
            if edge_data:
                edge = list(edge_data.values())[0]
                if 'geometry' in edge:
                    geom = edge['geometry']
                    if isinstance(geom, str):
                        geom = shapely.wkt.loads(geom)
                    coords = list(geom.coords)
                    if ruta_coords and ruta_coords[-1] == [coords[0][1], coords[0][0]]:
                        coords = coords[1:]
                    ruta_coords.extend([[c[1], c[0]] for c in coords])
                else:
                    punto_u = G.nodes[u]
                    punto_v = G.nodes[v]
                    if not ruta_coords or ruta_coords[-1] != [float(punto_u['y']), float(punto_u['x'])]:
                        ruta_coords.append([float(punto_u['y']), float(punto_u['x'])])
                    ruta_coords.append([float(punto_v['y']), float(punto_v['x'])])
        # Agregar segmento final si el último punto no es el destino exacto
        if ruta_coords and ruta_coords[-1] != [float(destino_coords[0]), float(destino_coords[1])]:
            ruta_coords.append([float(destino_coords[0]), float(destino_coords[1])])
        if not ruta_coords:
            return jsonify({"error": "No se pudo encontrar una ruta válida"}), 404
        return jsonify(ruta_coords)
    except Exception as e:
        print(f"Error en la ruta: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
