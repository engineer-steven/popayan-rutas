const map = L.map('map').setView([2.4429, -76.6060], 13); // Popayán

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);

let currentRoute = null;
let markers = [];
let lugares = {};

// Cargar lugares predefinidos
fetch('http://127.0.0.1:5000/lugares')
    .then(res => res.json())
    .then(data => {
        lugares = data;
        const selectOrigen = document.getElementById('origen');
        const selectDestino = document.getElementById('destino');
        
        // Llenar los selectores con los lugares
        Object.keys(lugares).forEach(lugar => {
            selectOrigen.add(new Option(lugar, lugar));
            selectDestino.add(new Option(lugar, lugar));
        });
    })
    .catch(err => {
        console.error('Error al cargar lugares:', err);
        alert('Error al cargar los lugares predefinidos');
    });

function limpiarMapa() {
    // Limpiar marcadores anteriores
    markers.forEach(marker => map.removeLayer(marker));
    markers = [];
    
    // Limpiar ruta anterior
    if (currentRoute) {
        map.removeLayer(currentRoute);
        currentRoute = null;
    }
}

function agregarMarcador(coords, titulo) {
    const marker = L.marker(coords)
        .bindPopup(titulo)
        .addTo(map);
    markers.push(marker);
    return marker;
}

function calcularRuta() {
    const origenSelect = document.getElementById('origen');
    const destinoSelect = document.getElementById('destino');
    
    const origenNombre = origenSelect.value;
    const destinoNombre = destinoSelect.value;
    
    if (!origenNombre || !destinoNombre) {
        alert('Por favor seleccione origen y destino');
        return;
    }
    
    if (origenNombre === destinoNombre) {
        alert('El origen y destino deben ser diferentes');
        return;
    }

    limpiarMapa();

    // Agregar marcadores
    const origenCoords = lugares[origenNombre];
    const destinoCoords = lugares[destinoNombre];
    const markerOrigen = agregarMarcador(origenCoords, `Origen: ${origenNombre}`);
    const markerDestino = agregarMarcador(destinoCoords, `Destino: ${destinoNombre}`);

    // Calcular y mostrar ruta
    fetch('http://127.0.0.1:5000/ruta', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            origen_nombre: origenNombre,
            destino_nombre: destinoNombre
        })
    })
    .then(res => {
        if (!res.ok) {
            throw new Error(`Error en la respuesta del servidor: ${res.status} ${res.statusText}`);
        }
        return res.json();
    })
    .then(data => {
        if (Array.isArray(data) && data.length > 0 && Array.isArray(data[0]) && data[0].length === 2) {
            currentRoute = L.polyline(data, { color: 'blue', weight: 5 }).addTo(map);
            map.fitBounds(currentRoute.getBounds());
            markerOrigen.openPopup();
        } else if (data.error) {
            alert('Error del servidor: ' + data.error);
        } else {
            alert('No se pudo encontrar una ruta entre los puntos seleccionados');
        }
    })
    .catch(err => {
        console.error('Error:', err);
        alert('Error al calcular la ruta: ' + err.message);
    });
}

// También permitir clicks en el mapa para puntos personalizados
map.on('click', (e) => {
    const lat = e.latlng.lat.toFixed(4);
    const lng = e.latlng.lng.toFixed(4);
    console.log(`Coordenadas: [${lat}, ${lng}]`);
});
