from image_processor import ImageProcessor
from file_finder import FileFinder
import os
import logging


# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
def main():

    file_finder = FileFinder()
    

    print("")    
    print("Choose to train the AI models or use the AI models to make 3D models with 3D photogrammetry")
    
    image_processor = ImageProcessor()
    while True:
        try:
            # Prompt the user for input
            name =  str(input("Type the name of the folder (recongized as the name of the object) inside \"Input\"\n"))
            checkName =file_finder.findFolder(name)
            # Check if the input is within the valid range
            if checkName != None:
                break  # Exit the loop if the input is valid
            else:
                logging.error("[main] - Invalid name! Please choose again!")
        except ValueError:
            # Handle the case where input is not an integer
            logging.error("[main] - Invalid name! Please enter a valid name.")
            
    image_processor.process_Images(file_finder, name)
if __name__ == "__main__":
    main()