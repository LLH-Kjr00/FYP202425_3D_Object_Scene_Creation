from denoiser_component import DenoiserComponent
import trimesh
import numpy as np
import gc
from scipy.sparse import lil_matrix  # For sparse matrix operations

class RemoveIsolatedDenoiser(DenoiserComponent):
    def __init__(self):
        pass

    def denoise(self, input_path, output_path, chunk_size=10000):
        print(f"[RemoveIsolated] - Removing isolated vertices in the mesh {input_path}...")

        # Load the model
        mesh = trimesh.load(input_path)
        if isinstance(mesh, trimesh.Scene):
            meshes = mesh.dump(concatenate=True)
        else:
            meshes = mesh

        # Show statistics before removal
        print(f'[RemoveIsolated] - Number of vertices before removal: {len(meshes.vertices)}')
        print(f'[RemoveIsolated] - Number of faces before removal: {len(meshes.faces)}')
        print(f'[RemoveIsolated] - Bounding box volume before removal: {meshes.bounding_box.volume}')
        print(f'[RemoveIsolated] - Surface area before removal: {meshes.area}')
        print("")

        # Process the mesh in chunks
        referenced_vertices = set()
        for i in range(0, len(meshes.faces), chunk_size):
            chunk_faces = meshes.faces[i:i + chunk_size]
            referenced_vertices.update(np.unique(chunk_faces))

        # Create a sparse mask for memory efficiency
        mask = lil_matrix((len(meshes.vertices), 1), dtype=bool)
        mask[list(referenced_vertices)] = True

        # Filter out the unreferenced vertices
        cleaned_vertices = meshes.vertices[mask.toarray().flatten()]
        new_indices = np.zeros(len(meshes.vertices), dtype=int)
        new_indices[mask.toarray().flatten()] = np.arange(len(cleaned_vertices))

        # Update faces to use the new indices
        cleaned_faces = new_indices[meshes.faces]

        # Create a new mesh with cleaned vertices and updated faces
        cleaned_mesh = trimesh.Trimesh(vertices=cleaned_vertices, faces=cleaned_faces)

       

        # Show statistics after removal
        print(f'[RemoveIsolated] - Number of vertices after removal: {len(cleaned_mesh.vertices)}')
        print(f'[RemoveIsolated] - Number of faces after removal: {len(cleaned_mesh.faces)}')
        print(f'[RemoveIsolated] - Bounding box volume after removal: {cleaned_mesh.bounding_box.volume}')
        print(f'[RemoveIsolated] - Surface area after removal: {cleaned_mesh.area}')
        print("")

        # Save the cleaned mesh back to GLB format
        cleaned_mesh.export(output_path)

        # Free memory
        del mask, referenced_vertices, new_indices, cleaned_mesh, mesh
        gc.collect()
        print(f"[RemoveIsolated] - Isolated vertices in the mesh {input_path} are removed!")
        print("")
        return output_path
