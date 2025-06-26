import os
from zipfile import ZipFile 
class FileZipper:
    def __init__(self):
   
        pass
    def get_all_file_paths(self, directory): 
    
        # initializing empty file paths list 
        file_paths = [] 
    
        # crawling through directory and subdirectories 
        for root, directories, files in os.walk(directory): 
            for filename in files: 
                # join the two strings in order to form the full filepath. 
                filepath = os.path.join(root, filename) 
                file_paths.append(filepath) 
    
        # returning all file paths 
        return file_paths         
    
    def zip_folder(self, folder_path, output_zip):
        
        # Step 1: Create a zip file containing all the files in the folder
        file_paths = self.get_all_file_paths(folder_path)
        with ZipFile(output_zip,'w') as zip: 
            # writing each file one by one 
           
            for file in file_paths: 
                print(file)
                zip.write(file) 
        print(f"[zip_folder] - Successfully zipped: {output_zip}")
        # Step 2: Delete all files inside the folder (but not the folder itself)
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                os.remove(file_path)  # Delete the file
        print(f"[zip_folder] - Successfully deleted: {folder_path}")
