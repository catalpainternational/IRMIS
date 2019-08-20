const headers = { 'Content-Type': 'application/json' };

function getRoadMetadata() {
    window.fetch(`${window.location.origin}/assets/roads`, { method: 'GET', headers })
        .then((response) => {
            if (response.ok) return response.json();
            throw new Error('Network response was not ok.');
        });
}

function getRoadGeometry(roadId) {
    window.fetch(`${window.location.origin}/assets/roads/${roadId.toString()}`, { method: 'GET', headers })
        .then((response) => {
            if (response.ok) return response.json();
            throw new Error('Network response was not ok.');
        });
}

exports = { getRoadMetadata, getRoadGeometry };
