from PIL import Image
import os 
import sys
import fnmatch
import numpy as np

#===definitions===

#initialize counting variables for successes, errors
success = 0
error = 0

def tif_to_rg_chromaticity(filename):
    try:
        #access the two variables
        global success, error
        #generate the path for the image being processed
        rgb_path = os.path.join(folder_path,filename)

        # Open the image
        rgb_image = Image.open(rgb_path)
        
        # Convert the image to RGB mode if it's not already
        if rgb_image.mode != 'RGB':
            rgb_image = rgb_image.convert('RGB')

        # Convert the image to numpy array
        rgb_array = np.array(rgb_image)

        # Calculate the chromaticity values: each channel divided by total pixel value (returns the proportion of each channed)
        total = np.sum(rgb_array, axis=2)
        total[total == 0] = 1  # Avoid division by zero

        r_chrom = rgb_array[:, :, 0] / total
        g_chrom = rgb_array[:, :, 1] / total
        b_chrom = 1 - r_chrom - g_chrom     #since the proportions add to 1

        # Scale the chromaticity values to 0-255 range
        r_chrom_scaled = (r_chrom * 255).astype(np.uint8)
        g_chrom_scaled = (g_chrom * 255).astype(np.uint8)
        b_chrom_scaled = (b_chrom * 255).astype(np.uint8)

        chroma_array = np.stack((r_chrom_scaled, g_chrom_scaled, b_chrom_scaled), axis=2)
        chromaticity_image = Image.fromarray(chroma_array)

        # create chromaticity file path
        chroma_path = os.path.join(chromaticity_folder, f'chromaticity_{filename}')
        chromaticity_image.save(chroma_path)

        #success
        success += 1
        print(f'{success}/{tif_count}: Successfuly converted {filename} to rgb chromaticity')
     

    except Exception as e: 
        error += 1
        print(f'Error processing {filename}: {e}')
        



#===main===

#get wd from user input
folder_path = input('Path to folder to convert?').strip('\"\'') #single and double quotes are OK

#check the wd is valid
if not os.path.isdir(folder_path):
    print('Invalid folder path. Please provide a valid directory path.')
    sys.exit()

#count the number of tif files to convert
tif_count = len(fnmatch.filter(os.listdir(folder_path), '*.tif')) + len(fnmatch.filter(os.listdir(folder_path), '*.tiff'))
print(f'There are {tif_count} .tif files to convert')

#create folder for chromaticity images
chromaticity_folder = os.path.join(folder_path, 'chromaticity')
os.makedirs(chromaticity_folder, exist_ok=True)

#convert files ending in .tif/.tiff             TODO: make this one list with the above function?
for filename in os.listdir(folder_path):
    if filename.endswith('.tif') or filename.endswith('.tiff'):
        tif_to_rg_chromaticity(filename)

    else:   
        print(f'Skipped {filename}: not a TIF file')

#Final message :)
print(f'Conversion complete: {success} successes, {error} errors')