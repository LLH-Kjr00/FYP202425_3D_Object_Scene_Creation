import cv2
import np
from multiprocessing import Pool
import logging
import os
# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
class ImageProcessor:
    
    def __init__(self):
        self.PreProcess_images = []
       
        pass
    
    def adjust_gamma(self, image, gamma):
        invGamma = 1.0 / gamma
        table = np.array([((i / 255.0) ** invGamma) * 255 for i in np.arange(0, 256)]).astype("uint8")
        return cv2.LUT(image, table)
    
    def adjust_brightness(self, image, brightness):
        return cv2.convertScaleAbs(image, alpha=1, beta=brightness)
    
    def adjust_constrast(self, image, constrast):
        return cv2.convertScaleAbs(image, alpha=constrast, beta=0)
    
    def adjust_color(self, image, r_factor, g_factor, b_factor):
        b, g, r = cv2.split(image)
        r = cv2.multiply(r, r_factor)
        g = cv2.multiply(g, g_factor)
        b = cv2.multiply(b, b_factor)
        return cv2.merge((b, g, r))
    
    def save_ProcessedImages(self, source, result, idx, subfolder):
        os.makedirs(f"Output/{subfolder}/", exist_ok=True)
        processed_source = "Processed_" + source
        cv2.imwrite(f"Output/{subfolder}/" + processed_source, result)
        logging.info(f"D[{idx}] -Processed {source} is now saved in \"Output//{subfolder}\"!") 
        
    def denoiseProcess(self, filename, idx, input_path, subfolder):
        img = cv2.imread(input_path + filename )
        logging.info(f"D[{idx}] -Start denoising {filename}...") 

        try:
            # Denoise
            logging.info(f"D[{idx}] - Denoising {filename} using filters..")
            denoised_Med = cv2.medianBlur(img, 3)
            denoised_Bil  = cv2.bilateralFilter(denoised_Med, 10, 20, 20)
            denoised_Gau = cv2.GaussianBlur(denoised_Bil, (7, 7), 0)
            logging.info(f"D[{idx}] - Denoising {filename} Completed!")
    
            # Adjust brightness and contrast
            logging.info(f"D[{idx}] - Adjusting {filename}'s parameters...")
            adjusted_bright = self.adjust_brightness(denoised_Gau, 1.2)
            adjusted_contrast = self.adjust_constrast(adjusted_bright, 1.2)
            adjusted_color = self.adjust_color(adjusted_contrast, 1.02, 1.02, 1.02)
            adjusted_gamma = self.adjust_gamma(adjusted_color, 1.5)
            logging.info(f"D[{idx}] - {filename}'s Adjustments Completed!")
            # Sharpen the image
            logging.info(f"D[{idx}] - Sharpening {filename}...")
            kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
            sharpened = cv2.filter2D(adjusted_gamma, -1, kernel)
            logging.info(f"D[{idx}] - Sharpening {filename} Completed!")
            self.save_ProcessedImages(filename, sharpened, idx, subfolder)
               
            logging.info(f"D[{idx}] -End denoising {filename}!") 

        except Exception as error:
            logging.error(f"D[{idx}] -The denoising of {filename} has some problems!")
            logging.error(f"D[{idx}] -Error in [process_Img]: " + str(error))
            
       
        
    def noiseReduction(self, input_path, subfolder):
        with Pool() as pool:
            pool.starmap(self.denoiseProcess, [(self.PreProcess_images[i], i, input_path, subfolder) for i in range(len(self.PreProcess_images))])
        logging.info("Finish Denoising!\n")

            
   
    def process_Images(self, file_finder, subfolder):
        try:
            input_path = "Input/"+subfolder+"/"
            
            print("")
            self.PreProcess_images = file_finder.find_Inputimage(input_path)
            logging.info("The input folder has the following images: ")
            print(self.PreProcess_images)
            print("")
            self.noiseReduction(input_path, subfolder)

           
        except Exception as error:
            logging.error("Something went wrong while processing the images!")
            logging.error(f"Error in [process_Images]: " + str(error))

    