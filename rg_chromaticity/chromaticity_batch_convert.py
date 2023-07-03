from PIL import Image
import os 
import sys
import fnmatch

#definitions

#initialize counting variables for successes, errors
success = 0
error = 0

def tif_to_rg_chromaticity(filename):
    try:
        global success, error
        rgb_path = os.path.join(folder_path,filename)

        # Open the rgb image
        rgb_image = Image.open(rgb_path)
        
        # Convert the image to RGB mode if it's not already
        if rgb_image.mode != 'RGB':
            rgb_image = rgb_image.convert('RGB')
        
        # Get the size of the image
        width, height = rgb_image.size
        
        # Create a new image for the chromaticity values
        chromaticity_image = Image.new('RGB', (width, height))
        
        # Iterate over each pixel in the image
        for y in range(height):
            for x in range(width):
                # Get the RGB values of the current pixel
                r, g, b = rgb_image.getpixel((x, y))
                
                # Calculate the chromaticity values
                total = r + g + b

                if total != 0:

                    r_chrom = r / total
                    g_chrom = g / total
                    b_chrom = b/total

                else: 

                    r_chrom = 0
                    g_chrom = 0
                    b_chrom = 0
                
                # Scale the chromaticity values to 0-255 range
                r_chrom_scaled = int(r_chrom * 255)
                g_chrom_scaled = int(g_chrom * 255)
                b_chrom_scaled = int(b_chrom * 255)
                
                # Set the chromaticity values as RGB values in the new image
                chromaticity_image.putpixel((x, y), (r_chrom_scaled, g_chrom_scaled, b_chrom_scaled))
        
        # create chromaticity file path
        chromaticity_path = os.path.join(chromaticity_folder, f'chromaticity_{filename}')
        chromaticity_image.save(chromaticity_path)

        success += 1
        print(f'{success}/{tif_count}: Successfuly converted {filename} to rgb chromaticity')

    except Exception as e: 
       error += 1
       print(f'Error processing {filename}: {e}')


#main

#get wd
folder_path = input('Path to folder to convert?').strip('\"\'')

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

#convert files ending in .tif/.tiff             RODO: make this one list with the above function?
for filename in os.listdir(folder_path):
    if filename.endswith('.tif') or filename.endswith('.tiff'):
        tif_to_rg_chromaticity(filename)

    else:   
        print(f'Unable to convert file: {filename} is not a TIF file')

print(f'Conversion complete')