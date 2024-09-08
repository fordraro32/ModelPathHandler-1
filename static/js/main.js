document.addEventListener('DOMContentLoaded', function() {
    const safetensorForm = document.getElementById('safetensor-form');
    const modelPathForm = document.getElementById('model-path-form');
    const listModelsForm = document.getElementById('list-models-form');
    const resultDiv = document.getElementById('result');

    safetensorForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const formData = new FormData(this);
        
        fetch('/upload', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                resultDiv.innerHTML = `<p style="color: red;">Error: ${data.error}</p>`;
            } else {
                resultDiv.innerHTML = `<p>File uploaded successfully!</p>
                                       <p>Metadata: ${JSON.stringify(data.metadata)}</p>`;
            }
        })
        .catch(error => {
            resultDiv.innerHTML = `<p style="color: red;">Error: ${error.message}</p>`;
        });
    });

    modelPathForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const formData = new FormData(this);
        
        fetch('/load_model', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                resultDiv.innerHTML = `<p style="color: red;">Error: ${data.error}</p>`;
            } else {
                resultDiv.innerHTML = `<p>Model loaded successfully!</p>
                                       <p>Model Info: ${JSON.stringify(data.model_info)}</p>`;
            }
        })
        .catch(error => {
            resultDiv.innerHTML = `<p style="color: red;">Error: ${error.message}</p>`;
        });
    });

    listModelsForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const directory = document.getElementById('directory').value;
        
        fetch(`/list_models?directory=${encodeURIComponent(directory)}`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                resultDiv.innerHTML = `<p style="color: red;">Error: ${data.error}</p>`;
            } else {
                resultDiv.innerHTML = `<p>Available models:</p>
                                       <ul>${data.models.map(model => `<li>${model}</li>`).join('')}</ul>`;
            }
        })
        .catch(error => {
            resultDiv.innerHTML = `<p style="color: red;">Error: ${error.message}</p>`;
        });
    });

    document.getElementById('get-model-info').addEventListener('click', function() {
        fetch('/model_info')
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                resultDiv.innerHTML = `<p style="color: red;">Error: ${data.error}</p>`;
            } else {
                resultDiv.innerHTML = `<p>Current Model Info:</p>
                                       <pre>${JSON.stringify(data, null, 2)}</pre>`;
            }
        })
        .catch(error => {
            resultDiv.innerHTML = `<p style="color: red;">Error: ${error.message}</p>`;
        });
    });
});
