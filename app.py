import os
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from utils.safe_tensor_manager import SafeTensorManager

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
db.init_app(app)

# Initialize SafeTensorManager
safe_tensor_manager = SafeTensorManager()

class Model(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    path = db.Column(db.String(500), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    parameters = db.Column(db.BigInteger, nullable=False)

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
        
        # Save model info to database
        new_model = Model(
            name=os.path.basename(model_path),
            path=model_path,
            type=model_info['type'],
            parameters=model_info['parameters']
        )
        db.session.add(new_model)
        db.session.commit()
        
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

@app.route('/save_model', methods=['POST'])
def save_model():
    output_path = request.form.get('output_path')
    if not output_path:
        return jsonify({'error': 'No output path provided'}), 400
    try:
        result = safe_tensor_manager.save_model_as_safetensors(output_path)
        return jsonify({'message': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/db_models', methods=['GET'])
def db_models():
    models = Model.query.all()
    return jsonify([{'id': model.id, 'name': model.name, 'path': model.path, 'type': model.type, 'parameters': model.parameters} for model in models])

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000)
