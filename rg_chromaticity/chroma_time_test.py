from PIL import Image
import numpy as np
import os 
import time
from datetime import timedelta

def tif_to_rg_chromaticity():
    try:
        start_time = time.monotonic()
        path = r'C:\Users\erwan\OneDrive\Desktop\Winter_4_1_ReferenceOnly_30x.tif'

        # Open the rgb image
        rgb_image = Image.open(path)

        # Convert the image to numpy array
        rgb_array = np.array(rgb_image)

        # Calculate the chromaticity values
        total = np.sum(rgb_array, axis=2)
        total[total == 0] = 1  # Avoid division by zero

        r_chrom = rgb_array[:, :, 0] / total
        g_chrom = rgb_array[:, :, 1] / total
        b_chrom = 1 - r_chrom - g_chrom

        # Scale the chromaticity values to 0-255 range
        r_chrom_scaled = (r_chrom * 255).astype(np.uint8)
        g_chrom_scaled = (g_chrom * 255).astype(np.uint8)
        b_chrom_scaled = (b_chrom * 255).astype(np.uint8)

        # Combine the channels into a new image
        chromaticity_array = np.stack((r_chrom_scaled, g_chrom_scaled, b_chrom_scaled), axis=2)
        chromaticity_image = Image.fromarray(chromaticity_array)

        # Create chromaticity file path
        chromaticity_path = os.path.join(r"C:\Users\erwan\OneDrive\Desktop", f'chroma_time_test.tif')
        chromaticity_image.save(chromaticity_path)

        end_time = time.monotonic()
        print(timedelta(seconds=end_time - start_time))

    except Exception as e: 
       print(f'oops: {e}')

tif_to_rg_chromaticity()