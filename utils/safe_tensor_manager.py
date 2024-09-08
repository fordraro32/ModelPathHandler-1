import os
import torch
from safetensors import safe_open
from safetensors.torch import save_file
from transformers import AutoModel

class SafeTensorManager:
    def __init__(self):
        self.current_model = None

    def load_safetensors(self, file):
        filename = file.filename
        file.save(filename)
        
        try:
            with safe_open(filename, framework="pt", device="cpu") as f:
                metadata = f.metadata()
                tensors = {k: f.get_tensor(k) for k in f.keys()}
            
            # Process or store tensors as needed
            # For now, we'll just return the metadata
            return metadata
        except Exception as e:
            raise Exception(f"Error loading SafeTensors file: {str(e)}")
        finally:
            # Clean up the temporary file
            if os.path.exists(filename):
                os.remove(filename)

    def load_model(self, model_path):
        try:
            # Check if the path exists
            if not os.path.exists(model_path):
                raise FileNotFoundError(f"Model path does not exist: {model_path}")

            # Check if it's a directory (for models saved with save_pretrained)
            if os.path.isdir(model_path):
                # Assume it's a Hugging Face model
                self.current_model = AutoModel.from_pretrained(model_path)
            elif model_path.endswith('.safetensors'):
                # Load SafeTensors file
                with safe_open(model_path, framework="pt", device="cpu") as f:
                    tensors = {k: f.get_tensor(k) for k in f.keys()}
                self.current_model = AutoModel.from_pretrained(None, state_dict=tensors)
            else:
                # Assume it's a PyTorch model
                self.current_model = torch.load(model_path)

            # Get model info
            model_info = self.get_model_info()

            return model_info
        except Exception as e:
            raise Exception(f"Error loading model: {str(e)}")

    def get_model_info(self):
        if self.current_model is None:
            raise Exception("No model loaded. Please load a model first.")

        model_info = {
            "type": type(self.current_model).__name__,
            "parameters": sum(p.numel() for p in self.current_model.parameters()),
            "state_dict_keys": list(self.current_model.state_dict().keys())
        }

        return model_info

    def save_model_as_safetensors(self, output_path):
        if self.current_model is None:
            raise Exception("No model loaded. Please load a model first.")

        try:
            state_dict = self.current_model.state_dict()
            save_file(state_dict, output_path)
            return f"Model saved as SafeTensors at {output_path}"
        except Exception as e:
            raise Exception(f"Error saving model as SafeTensors: {str(e)}")

    def list_models(self, directory):
        try:
            models = []
            for root, dirs, files in os.walk(directory):
                for file in files:
                    if file.endswith(('.pt', '.pth', '.bin', '.safetensors')):
                        models.append(os.path.join(root, file))
            return models
        except Exception as e:
            raise Exception(f"Error listing models: {str(e)}")
