from model_loader import ModelLoader
from model_denoiser import ModelDenoiser
from model_exporter import ModelExporter
from file_finder import FileFinder
from file_zipper import FileZipper
import os

def main():
    
    input_folder = "Input/"

    model_denoiser = ModelDenoiser()
    model_exporter = ModelExporter()
    file_finder = FileFinder()
    file_zipper = FileZipper()
    print("[main] - Finding OBJ files to denoise... (Other formats are NOT SUPPORTED)")
    base_name_list, path_list = file_finder.find_InputModel(input_folder)
    
    if (len(path_list) <= 0): 
        print("[main] - No model to denoise!")
    else:
        while True:
            try:
                # Prompt the user for input
                isAuto =  float(input("Press 0 for auto mode (use pre-set parameters) or Press 1 for manual mode (manually set the parameters)\n"))
                
                # Check if the input is within the valid range
                if isAuto == 0:
                    for i in range(len(path_list)): #len(path_list)
                        # Load the model
                        # model = model_loader.load_str_model(input_path)
                        # model_loader.show_str_model(model)

                        print(f"[main] - Start denosing model named {base_name_list[i]} in {path_list[i]}...")

                        # Denoise the model
                        output_path = model_denoiser.denoise_all_auto(path_list[i], base_name_list[i])

                        # Show the denoised model 
                        print(f"[main] - Denosing of model named {base_name_list[i]} in {path_list[i]} completed!")
                        
                        denoised_model = model_exporter.load_fin_model(output_path)
                        #model_exporter.show_fin_model(denoised_model)
                    break  # Exit the loop if the input is valid
                elif isAuto == 1:
                    for i in range(len(path_list)): #len(path_list)
                        
                        model_loader = ModelLoader()
                        
                        #Load the model
                        model = model_loader.load_str_model(path_list[i])
                        model_loader.show_str_model(model)

                        print(f"[main] - Start denosing model named {base_name_list[i]} in {path_list[i]}...")

                        # Denoise the model
                        output_path = model_denoiser.denoise_all_manual(path_list[i], base_name_list[i])

                        # Show the denoised model 
                        print(f"[main] - Denosing of model named {base_name_list[i]} in {path_list[i]} completed!")
                        
                        denoised_model = model_exporter.load_fin_model(output_path)
                        model_exporter.show_fin_model(denoised_model)
                        
                    break  # Exit the loop if the input is valid
                else:
                    print("[main] - Invalid value! Please choose again!")
            except ValueError:
                # Handle the case where input is not an integer
                print("[denoise_all] - Invalid input! Please enter a valid integer value.")  
        

            
    all_entries = os.listdir("Output/Intermediate/")
    
    # Filter and count only directories
    folder_names = [entry for entry in all_entries if os.path.isdir(os.path.join("Output/Intermediate/", entry))]
    
    for name in folder_names: 
        folder_to_zip = f"Output/Intermediate/{name}/"
        
        output_zip_file = f"Output/Zips/{name}.zip"
        file_zipper.zip_folder(folder_to_zip, output_zip_file)
        print(f"[main] - All files in {folder_to_zip} are zipped into {output_zip_file}")
    
if __name__ == "__main__":
    main()
