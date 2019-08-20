const headers = { 'Content-Type': 'application/json' };

async function getRoadMetadata() {
    return window.fetch(`${window.location.origin}/assets/roads`, { method: 'GET', headers })
        .then((response) => {
            if (response.ok) return response.json();
            throw new Error('Network response was not ok.');
        }).then(json => json);
}

async function getRoadGeometry(roadId) {
    return window.fetch(`${window.location.origin}/assets/roads/${roadId.toString()}`, { method: 'GET', headers })
        .then((response) => {
            if (response.ok) return response.json();
            throw new Error('Network response was not ok.');
        }).then(json => json);
}

exports = { getRoadMetadata, getRoadGeometry };
