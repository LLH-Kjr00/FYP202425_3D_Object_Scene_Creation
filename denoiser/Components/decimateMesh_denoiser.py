from denoiser_component import DenoiserComponent
import numpy as np
import pyvista as pv
import fast_simplification
import gc
class DecimateMeshDenoiser(DenoiserComponent):
    def __init__(self):
    
            pass
    def denoise(self, input_path, output_path, target_reduction):
        print(f"[DecimateMesh] - Decimating the mesh {input_path}...")

        # Load the Model
        mesh = pv.read(input_path)
        print("[DecimateMesh] - Metrics BEFORE decimation:")

        self.print_mesh_metrics(mesh)

        #mesh.plot()
        points = mesh.points
        triangles = mesh.faces.reshape(-1, 4)[:, 1:]
        print(f"[DecimateMesh] - Decimating the mesh by reducing {target_reduction*100}% of the total number of vertices...")
        dec_points, dec_triangles, collapses = fast_simplification.simplify(points, triangles, target_reduction, return_collapses=True)
        # Create a new PyVista mesh from the decimated points and triangles
        print(f"[DecimateMesh] - Creating a new mesh from the decimated points and triangles...")
        dec_mesh = pv.PolyData(dec_points, np.hstack([np.full((dec_triangles.shape[0], 1), 3), dec_triangles]))
        # dec_mesh.plot()
        # Save the decimated mesh
        print(f"[DecimateMesh] - Decimated mesh is saved to {output_path}.")
        dec_mesh.save(output_path)

        # Calculate and print metrics
        print("[DecimateMesh] - Metrics AFTER decimation:")

        self.print_mesh_metrics(dec_mesh)

        del mesh, points, triangles, dec_points, dec_triangles, collapses
        gc.collect()
        print(f"[DecimateMesh] - Decimated the mesh {input_path}!")
        print("")
        return output_path

    def print_mesh_metrics(self, mesh):
        # Number of vertices
        num_vertices = mesh.n_points
        # Number of edges (assuming a triangular mesh)
        num_edges = mesh.n_faces_strict * 3 // 2
        # Number of surfaces (polygons)
        num_surfaces = mesh.n_faces_strict

        print(f"[DecimateMesh] - Number of vertices: {num_vertices}")
        print(f"[DecimateMesh] - Number of edges: {num_edges}")
        print(f"[DecimateMesh] - Number of surfaces (polygons): {num_surfaces}")