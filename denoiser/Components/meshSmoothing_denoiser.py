from denoiser_component import DenoiserComponent
import open3d as o3d
import gc
import numpy as np

class MeshSmoothingDenoiser(DenoiserComponent):
    def __init__(self):
        pass

    def denoise(self, input_path, output_path, iterations):
        gc.disable()  # Disable garbage collector for performance

        # Load and process the mesh
        model = o3d.io.read_triangle_mesh(input_path)
        # Calculate metrics before smoothing
        
        
        print(f"[MeshSmoothing] - Smoothing the mesh {input_path}...")

        smoothed_model = model.filter_smooth_taubin(iterations)
        o3d.io.write_triangle_mesh(output_path, smoothed_model)

        # Calculate metrics after smoothing
        
        self.print_smoothing_metrics(model,smoothed_model)

        # Free memory
        del model
        gc.enable()  # Re-enable garbage collector
        gc.collect()

        print(f"[MeshSmoothing] - Mesh {input_path} is smoothed!")
        print("")
        return output_path
        
    def print_smoothing_metrics(self, mesh, smoothed_mesh):
        # Surface roughness
        roughness = self.calculate_surface_roughness(mesh,smoothed_mesh )
        print(f"[MeshSmoothing] - Surface roughness: {roughness:.4f}")

        print("[MeshSmoothing] - Metrics BEFORE smoothing:")
        # Edge length variance
        edge_variance = self.calculate_edge_length_variance(mesh)
        print(f"[MeshSmoothing] - Edge length variance: {edge_variance:.4f}")
        print("[MeshSmoothing] - Metrics AFTER smoothing:")
        # Edge length variance
        edge_variance = self.calculate_edge_length_variance(smoothed_mesh)
        print(f"[MeshSmoothing] - Edge length variance: {edge_variance:.4f}")

    

    def calculate_edge_length_variance(self, mesh):
        # Extract vertices and triangles
        vertices = np.asarray(mesh.vertices)
        triangles = np.asarray(mesh.triangles)

        # Calculate edges from triangles
        edges = []
        for triangle in triangles:
            edges.append([triangle[0], triangle[1]])
            edges.append([triangle[1], triangle[2]])
            edges.append([triangle[2], triangle[0]])
        edges = np.unique(edges, axis=0)

        # Calculate edge lengths
        edge_lengths = np.linalg.norm(vertices[edges[:, 0]] - vertices[edges[:, 1]], axis=1)

        # Calculate variance of edge lengths
        edge_variance = np.var(edge_lengths)
        return edge_variance
    
    def calculate_surface_roughness(self, mesh, smoothed_mesh):
        
        # Step 2: Calculate deviations
        original_vertices = np.asarray(mesh.vertices)
        smoothed_vertices = np.asarray(smoothed_mesh.vertices)
        deviations = np.linalg.norm(original_vertices - smoothed_vertices, axis=1)

        # Step 3: Compute RMS of deviations
        surface_roughness = np.sqrt(np.mean(deviations**2))
        return surface_roughness