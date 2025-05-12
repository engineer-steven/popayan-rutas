import osmnx as ox
import networkx as nx
from math import radians, sin, cos, sqrt, atan2
import numpy as np

def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371  # Radio de la Tierra en kilómetros
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    return R * c

def encontrar_nodo_mas_cercano(G, lat, lon, radio_max=2.0, modo='origen'):
    """Encuentra el nodo más cercano ACCESIBLE según el sentido de la vía (modo='origen' o 'destino')."""
    radio_grados = radio_max / 111.32
    lat_min, lat_max = lat - radio_grados, lat + radio_grados
    lon_min, lon_max = lon - radio_grados, lon + radio_grados
    nodos_candidatos = []
    for node, data in G.nodes(data=True):
        nlat = float(data['y'])
        nlon = float(data['x'])
        if lat_min <= nlat <= lat_max and lon_min <= nlon <= lon_max:
            dist = haversine_distance(lat, lon, nlat, nlon)
            if dist < radio_max:
                # Solo nodos accesibles según el sentido de la vía
                if modo == 'origen' and len(list(G.successors(node))) > 0:
                    nodos_candidatos.append((node, dist))
                elif modo == 'destino' and len(list(G.predecessors(node))) > 0:
                    nodos_candidatos.append((node, dist))
    if not nodos_candidatos:
        radio_grados = (radio_max * 2) / 111.32
        lat_min, lat_max = lat - radio_grados, lat + radio_grados
        lon_min, lon_max = lon - radio_grados, lon + radio_grados
        for node, data in G.nodes(data=True):
            nlat = float(data['y'])
            nlon = float(data['x'])
            if lat_min <= nlat <= lat_max and lon_min <= nlon <= lon_max:
                dist = haversine_distance(lat, lon, nlat, nlon)
                if dist < radio_max * 2:
                    if modo == 'origen' and len(list(G.successors(node))) > 0:
                        nodos_candidatos.append((node, dist))
                    elif modo == 'destino' and len(list(G.predecessors(node))) > 0:
                        nodos_candidatos.append((node, dist))
    if not nodos_candidatos:
        return None, None
    nodos_candidatos.sort(key=lambda x: x[1])
    return nodos_candidatos[0]  # (node, dist)

def calcular_ruta_mas_corta(G, origen, destino):
    try:
        lat1, lon1 = origen
        lat2, lon2 = destino
        print(f"Buscando nodos cercanos a: Origen({lat1}, {lon1}), Destino({lat2}, {lon2})")
        orig_node, orig_dist = encontrar_nodo_mas_cercano(G, lat1, lon1, radio_max=2.0, modo='origen')
        dest_node, dest_dist = encontrar_nodo_mas_cercano(G, lat2, lon2, radio_max=2.0, modo='destino')
        if orig_node is None or dest_node is None:
            return []
        ruta_nodos = nx.shortest_path(G, orig_node, dest_node, weight='length')
        ruta_coords = []
        for node in ruta_nodos:
            point = G.nodes[node]
            ruta_coords.append([float(point['y']), float(point['x'])])
        return ruta_coords
    except Exception as e:
        print(f"Error al calcular la ruta: {str(e)}")
        return []

def encontrar_nodo_destino_correcto(G, lat, lon, origen_nodo, radio_max=2.0):
    """Busca entre varios nodos cercanos al destino el que permita llegar en el sentido correcto y minimiza la distancia total."""
    radio_grados = radio_max / 111.32
    lat_min, lat_max = lat - radio_grados, lat + radio_grados
    lon_min, lon_max = lon - radio_grados, lon + radio_grados
    nodos_candidatos = []
    for node, data in G.nodes(data=True):
        nlat = float(data['y'])
        nlon = float(data['x'])
        if lat_min <= nlat <= lat_max and lon_min <= nlon <= lon_max:
            dist = haversine_distance(lat, lon, nlat, nlon)
            if dist < radio_max:
                # Solo nodos accesibles como destino (tienen predecesores)
                if len(list(G.predecessors(node))) > 0:
                    nodos_candidatos.append((node, dist, nlat, nlon))
    # Si no hay candidatos en el radio, buscar en todo el grafo
    if not nodos_candidatos:
        for node, data in G.nodes(data=True):
            nlat = float(data['y'])
            nlon = float(data['x'])
            dist = haversine_distance(lat, lon, nlat, nlon)
            if len(list(G.predecessors(node))) > 0:
                nodos_candidatos.append((node, dist, nlat, nlon))
    if not nodos_candidatos:
        return None, None, None
    mejor_ruta = None
    mejor_nodo = None
    mejor_dist = None
    mejor_total = float('inf')
    for node, dist, nlat, nlon in nodos_candidatos:
        try:
            ruta_nodos = nx.shortest_path(G, origen_nodo, node, weight='length')
            # Distancia total: ruta + segmento final al destino
            dist_total = nx.shortest_path_length(G, origen_nodo, node, weight='length') + dist
            if dist_total < mejor_total:
                mejor_total = dist_total
                mejor_ruta = ruta_nodos
                mejor_nodo = node
                mejor_dist = dist
        except Exception:
            continue
    return mejor_nodo, mejor_dist, mejor_ruta
