import os 
class FileFinder:
    def __init__(self):
        pass
    def is_valid_image_extension(self, file_name):
        # Check the file if it has an image format or not, return True if so
        valid_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp'}
        return any(file_name.lower().endswith(ext) for ext in valid_extensions)
    
    def find_Inputimage (self, file_path):
        img_list = []
        for path in os.listdir(file_path):
            check_file = os.path.join(file_path, path)
            # Check if the current instance in the Input folder is a image file or not
            if os.path.isfile(check_file) and self.is_valid_image_extension(check_file) == True:
                base_name = os.path.basename(check_file)
                img_list.append(base_name)
        return img_list
    def findFolder(self,folderName):
        input_folderDir = "Input/"
        for root, dirs, files in os.walk(input_folderDir):
            if folderName in dirs:
                return os.path.join(root, folderName)
        return None
                
