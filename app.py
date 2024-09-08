import os
from flask import Flask, render_template, request, jsonify
from utils.safe_tensor_manager import SafeTensorManager

app = Flask(__name__)

# Initialize SafeTensorManager
safe_tensor_manager = SafeTensorManager()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_safetensors():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file:
        try:
            metadata = safe_tensor_manager.load_safetensors(file)
            return jsonify({'message': 'File uploaded successfully', 'metadata': metadata})
        except Exception as e:
            return jsonify({'error': str(e)}), 400

@app.route('/load_model', methods=['POST'])
def load_model():
    model_path = request.form.get('model_path')
    if not model_path:
        return jsonify({'error': 'No model path provided'}), 400
    try:
        model_info = safe_tensor_manager.load_model(model_path)
        return jsonify({'message': 'Model loaded successfully', 'model_info': model_info})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/list_models', methods=['GET'])
def list_models():
    directory = request.args.get('directory', '.')
    try:
        models = safe_tensor_manager.list_models(directory)
        return jsonify({'models': models})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/model_info', methods=['GET'])
def model_info():
    try:
        info = safe_tensor_manager.get_model_info()
        return jsonify(info)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
