import os 
class FileFinder:
    def __init__(self):
   
        pass

    def is_valid_OBJ_extension(self, file_name):
        # Check the file if it has an image format or not, return True if so
        valid_extensions = {'obj'}
        return any(file_name.lower().endswith(ext) for ext in valid_extensions)
    
    def find_InputModel (self, file_path):
        base_name_list =[]
        path_list =[]
        base_name = None
        for path in os.listdir(file_path):
            check_file = os.path.join(file_path, path)
            # Check if the current instance in the Input folder is a image file or not
            if os.path.isfile(check_file) and self.is_valid_OBJ_extension(check_file) == True:
                try:
                    # Extract the base name without extension
                    base_name = os.path.splitext(os.path.basename(check_file))[0]
                except:
                # Give a default name for models having undecodable filename 
                    base_name = "Loaded_Model_" + path_list.count
                base_name_list.append(base_name)
                path_list.append(check_file)
        
        return base_name_list, path_list
               