// static/js/script.js

document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('predictionForm').addEventListener('submit', function(event) {
        event.preventDefault();
        var features = document.getElementById('features').value.split(',').map(Number);
        fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ features: features })
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById('result').textContent = 'Prediction: ' + data.prediction;
        });
    });
});
