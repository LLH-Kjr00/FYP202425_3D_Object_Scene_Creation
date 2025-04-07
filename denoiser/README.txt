How to Install the 3D Model Denoiser:
1. Download the ZIP file  
2. Extract the ZIP file 
3. Open a compiler (Preferably Microsoft Visual Studio Code)
4. Open the file directory where "denoiser_App.py" is
5. Run "pip install -r requirements.txt" to install all the required libraries 
6. If there is a dependency conflict when installing the "fast-simplification" library, ignore it
7. Installation is finished, ready for denoising 

How to Use the 3D Model Denoiser:
1. Load the 3D models in OBJ format into the “Input” Folder (without sub-folders), including the texture images and the MTL files
2. Run denoiser_App.py
3. Choose the operation mode by pressing 0 or 1
3a. Press 0 for automatic process with predefined parameters, suitable for scanned room models in general 
3b. Press 1 for manual process with self-defined parameters, suitable for smaller objects or objects with a lot of holes 
4a. If you pressed 0, just wait for the process to be finished 
4b. If you pressed 1, input appropriate values in the terminal and wait for the process to be finished	
5. Denoising is finished, ready for further processing in the Blender Python Script 

How to Install the Texture-Baking Blender Python Script:
1. Download the ZIP file  
2. Extract the ZIP file 
3. Install the latest version of Blender (Tested on from 4.2 to 4.4)
6. Installation is finished, ready for texture baking 

How to Use the Texture-Baking Blender Python Script:
1. Open the "bakeTexture.blend" file under the file directory "Blender_BakeTexture/"
2. Run the Script under “Scripting” 
3. Wait for a moment to load all the input and output pairs of models 
4. Hide all model pairs that you are not currently working with and only show the pair that you want to work with
5. Select the image textures of the models you are working with under “Shading” 
6. Choose the original model first, then press “Ctrl” and choose the denoised model (Caution: First choosing original model then the denoised model, THE ORDER CANNOT BE REVERSED)
7. Go to “Render” and press “Bake”
8. Wait for a moment for baking the texture
9. Repeat Step 3 to 9 for other pairs of models
10. Texture-baking is finished, ready for importing the denoised and texturized models for usage

