import trimesh

class ModelExporter:
    def __init__(self):
   
        pass
    def prompt_desired_format(self):
        # Logic for prompting desired format
        pass

    def export_as_gltf(self, model, save_path):
        model.export(save_path, file_type='gltf')
        print(f"Model exported as GLTF to {save_path}")
    def export_as_obj(self, model, save_path):
        model.export(save_path, file_type='obj')
        print(f"Model exported as OBJ to {save_path}")

    def load_fin_model(self, path: str):
        model = trimesh.load(path, force='mesh')
        print(f"Model loaded from {path}")
        return model
    
    def show_fin_model(self, model):
        model.show()
        print("Model displayed.")
    def decide_Format(self, model, format, path):
        match format:
            case "obj":
                self.export_as_gltf(model, path)

            case "gltf":
                self.export_as_gltf(model, path)

            