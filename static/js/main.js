document.addEventListener('DOMContentLoaded', function() {
    const safetensorForm = document.getElementById('safetensor-form');
    const modelPathForm = document.getElementById('model-path-form');
    const listModelsForm = document.getElementById('list-models-form');
    const saveModelForm = document.getElementById('save-model-form');
    const resultDiv = document.getElementById('result');
    const getDbModelsButton = document.getElementById('get-db-models');
    const dbModelsListDiv = document.getElementById('db-models-list');

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
                                       <p>Metadata: ${JSON.stringify(data.metadata, null, 2)}</p>`;
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
                                       <p>Model Info:</p>
                                       <pre>${JSON.stringify(data.model_info, null, 2)}</pre>`;
                refreshDbModels();
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

    saveModelForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const formData = new FormData(this);
        
        fetch('/save_model', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                resultDiv.innerHTML = `<p style="color: red;">Error: ${data.error}</p>`;
            } else {
                resultDiv.innerHTML = `<p>${data.message}</p>`;
            }
        })
        .catch(error => {
            resultDiv.innerHTML = `<p style="color: red;">Error: ${error.message}</p>`;
        });
    });

    getDbModelsButton.addEventListener('click', refreshDbModels);

    function refreshDbModels() {
        fetch('/db_models')
        .then(response => response.json())
        .then(data => {
            if (data.length === 0) {
                dbModelsListDiv.innerHTML = '<p>No models in the database.</p>';
            } else {
                const tableHTML = `
                    <table>
                        <tr>
                            <th>Name</th>
                            <th>Path</th>
                            <th>Type</th>
                            <th>Parameters</th>
                        </tr>
                        ${data.map(model => `
                            <tr>
                                <td>${model.name}</td>
                                <td>${model.path}</td>
                                <td>${model.type}</td>
                                <td>${model.parameters}</td>
                            </tr>
                        `).join('')}
                    </table>
                `;
                dbModelsListDiv.innerHTML = tableHTML;
            }
        })
        .catch(error => {
            dbModelsListDiv.innerHTML = `<p style="color: red;">Error: ${error.message}</p>`;
        });
    }

    // Initial load of DB models
    refreshDbModels();
});
