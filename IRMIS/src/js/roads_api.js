const headers = { 'Content-Type': 'application/json' };

function getRoadMetadata() {
    window.fetch(`${window.location.origin}/assets/roads`, { method: 'GET', headers })
        .then(response => response.json());
}

function getRoadGeometry(roadId) {
    window.fetch(`${window.location.origin}/assets/roads/${roadId.toString()}`, { method: 'GET', headers })
        .then(response => response.json());
}

exports = { getRoadMetadata, getRoadGeometry };
