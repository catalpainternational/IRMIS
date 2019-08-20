const headers = { 'Content-Type': 'application/json' };

function getRoadMetadata() {
    window.fetch('http://127.0.0.1:8000/assets/roads', { method: 'GET', headers })
        .then(response => response.json());
}

function getRoadGeometry(roadId) {
    window.fetch(`http://127.0.0.1:8000/assets/roads/${roadId.toString()}`, { method: 'GET', headers })
        .then(response => response.json());
}

module.exports = { getRoadMetadata, getRoadGeometry };
