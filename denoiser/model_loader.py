import trimesh

class ModelLoader:
    def __init__(self):
        pass
    
    def load_str_model(self, path: str):
        model = trimesh.load(path, force='mesh')
        print(f"Model loaded from {path}")
        return model

    def show_str_model(self, model):
        model.show()
        print("Model displayed.")
