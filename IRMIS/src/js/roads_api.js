const headers = { 'Content-Type': 'application/json' };

function getRoadMetadata() {
    return window.fetch(`${window.location.origin}/assets/roads`, { method: 'GET', headers })
        .then((response) => {
            if (response.ok) return response.json();
            throw new Error('Network response was not ok.');
        }).then(json => json);
}

function getRoadGeometry(roadId) {
    return window.fetch(`${window.location.origin}/assets/roads/${roadId}`, { method: 'GET', headers })
        .then((response) => {
            if (response.ok) return response.json();
            throw new Error('Network response was not ok.');
        }).then(json => json);
}

exports = { getRoadMetadata, getRoadGeometry };
