
from denoiser_component import DenoiserComponent
from pymeshfix import _meshfix
import pyvista as pv

class HoleFillingDenoiser(DenoiserComponent):
    def __init__(self):
        pass

    def denoise(self, input_path, output_path, strength):
        
        mesh = pv.read(input_path)
        print("[HoleFilling] - Metrics BEFORE hole filling:")
        self.print_hole_metrics(mesh)
        tin = _meshfix.PyTMesh()
       
        # Load the mesh file
        tin.load_file(input_path)

        # Apply hole filling
        print(f"[HoleFilling] - Filling holes in the mesh {input_path}...")
        tin.fill_small_boundaries(nbe=strength, refine=True)

        # Save the modified mesh
        tin.save_file(output_path)
        print(f"[HoleFilling] - Holes in the mesh {input_path} are filled!")
        print("")

        # Load the filled mesh using PyVista to calculate metrics
        filled_mesh = pv.read(output_path)
        print("[HoleFilling] - Metrics AFTER hole filling:")
        self.print_hole_metrics(filled_mesh)

        return output_path
    
    def print_hole_metrics(self, mesh):
        # Number of holes (open edges)
        num_holes = mesh.n_open_edges
        # Area of holes (boundary edges)
        boundary_edges = mesh.extract_feature_edges(boundary_edges=True, feature_edges=False, manifold_edges=False)
        hole_area = boundary_edges.area

        print(f"[HoleFilling] - Number of holes: {num_holes}")
        print(f"[HoleFilling] - Total hole area: {hole_area:.2f}")
        print("")