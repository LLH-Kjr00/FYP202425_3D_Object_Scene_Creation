from Components.holeFilling_denoiser import HoleFillingDenoiser
from Components.removeIsolated_denoiser import RemoveIsolatedDenoiser
from Components.meshSmoothing_denoiser import MeshSmoothingDenoiser
from Components.decimateMesh_denoiser import DecimateMeshDenoiser

class ModelDenoiser:
    def __init__(self):
        self.hole_filling_denoiser = HoleFillingDenoiser()
        self.remove_isolated_denoiser = RemoveIsolatedDenoiser()
        self.mesh_smoothing_denoiser = MeshSmoothingDenoiser()
        self.decimate_mesh_denoiser = DecimateMeshDenoiser()

    def denoise_all_manual(self, input_path, base_name):

        process_path = None

        process_path = self.remove_isolated_denoiser.denoise(input_path, f"Output/Intermediate/RmvIsoVertice/{base_name}_removedIsolated.obj") 

        print("[denoise_all] - What is the targeted strength for filling holes? (Larger value means filling bigger holes)")
        print("")
        while True:
            try:
                # Prompt the user for input
                target_fillLv = int(input("Input an integer number x, where 200 <= x <= 2000\n"))
                
                # Check if the input is within the valid range
                if 200 <= target_fillLv <= 2000:
                    break  # Exit the loop if the input is valid
                else:
                    print("[denoise_all] - Invalid fill-hole strength value! Please choose again!")
            except ValueError:
                # Handle the case where input is not an integer
                print("[denoise_all] - Invalid input! Please enter a valid integer.")
        print("")
        process_path = self.hole_filling_denoiser.denoise(process_path, f"Output/Intermediate/FillingHoles/{base_name}_holeFilled.obj", target_fillLv)
        
        print("[denoise_all] - What is the targeted smoothing iteration? (More iteration means stronger smoothing)")
        print("")
        while True:
            try:
                # Prompt the user for input
                target_smoothness = int(input("Input an integer number x, where 0 < x <= 10\n"))
                
                # Check if the input is within the valid range
                if 0 < target_smoothness <= 10:
                    break  # Exit the loop if the input is valid
                else:
                    print("[denoise_all] - Invalid smoothing iteration value! Please choose again!")
            except ValueError:
                # Handle the case where input is not an integer
                print("[denoise_all] - Invalid input! Please enter a valid integer.")
        print("")
        process_path = self.mesh_smoothing_denoiser.denoise(process_path, f"Output/Intermediate/MeshSmoothing/{base_name}_smoothen.obj", target_smoothness) 

        print("[denoise_all] - What is the targeted decimation level? (Larger number means stronger decimation)")
        print("")
        while True:
            try:
                # Prompt the user for input
                target_decimation =  float(input("Input an integer number x, where 0 <= x < 1\n"))
                
                # Check if the input is within the valid range
                if 0 <= target_decimation < 1:
                    break  # Exit the loop if the input is valid
                else:
                    print("[denoise_all] - Invalid targeted decimation value! Please choose again!")
            except ValueError:
                # Handle the case where input is not an integer
                print("[denoise_all] - Invalid input! Please enter a valid float value.")  
        print("")      
        process_path = self.decimate_mesh_denoiser.denoise(process_path, f"Output/Finished/{base_name}_finished.obj", target_decimation)
        
        output_path  = process_path

        return output_path
    def denoise_all_auto(self, input_path, base_name):

        process_path = None

        process_path = self.remove_isolated_denoiser.denoise(input_path, f"Output/Intermediate/RmvIsoVertice/{base_name}_removedIsolated.obj") 
        target_fillLv = 2000 #int(input("Input an integer number x, where 200 <= x <= 2000\n"))
        process_path = self.hole_filling_denoiser.denoise(process_path, f"Output/Intermediate/FillingHoles/{base_name}_holeFilled.obj", target_fillLv)
        print("")

        target_smoothness = 10 #int(input("Input an integer number x, where 0 < x <= 10\n"))
        process_path = self.mesh_smoothing_denoiser.denoise(process_path, f"Output/Intermediate/MeshSmoothing/{base_name}_smoothen.obj", target_smoothness)        
        print("")

        target_decimation =  0.85 #float(input("Input an integer number x, where 0 <= x < 1\n"))
        process_path = self.decimate_mesh_denoiser.denoise(process_path, f"Output/Finished/{base_name}_finished.obj", target_decimation)
        print("")      
        
        output_path  = process_path

        return output_path
    