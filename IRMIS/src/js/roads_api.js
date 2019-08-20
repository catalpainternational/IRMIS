const fetch = require('node-fetch');

var headers = {
    "Content-Type": "application/json",
    "Authorization": "Basic " + btoa("username:password"),
}

function getRoadMetadata() {
    fetch('http://127.0.0.1:8000/assets/roads', { method: 'GET', headers: headers })
    .then(function(response) {
        console.log(response);
        return response.json();
    }).then(function(json) {
        console.log(json);
    });
}

function getRoadGeometry(roadId) {
    fetch('http://127.0.0.1:8000/assets/roads/' + roadId.toString(), { method: 'GET', headers: headers })
    .then(function(response) {
        console.log(response);
        return response.json();
    }).then(function(json) {
        console.log(json);
    });
}

module.exports = { getRoadMetadata, getRoadGeometry };
