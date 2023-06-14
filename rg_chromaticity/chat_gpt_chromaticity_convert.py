from PIL import Image

def tif_to_rg_chromaticity(tif_path):
    # Open the TIFF image
    image = Image.open(tif_path)
    
    # Convert the image to RGB mode if it's not already
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    # Get the size of the image
    width, height = image.size
    
    # Create a new image for the chromaticity values
    chromaticity_image = Image.new('RGB', (width, height))
    
    # Iterate over each pixel in the image
    for y in range(height):
        for x in range(width):
            # Get the RGB values of the current pixel
            r, g, b = image.getpixel((x, y))
            
            # Calculate the chromaticity values
            total = r + g + b
            r_chrom = r / total
            g_chrom = g / total
            b_chrom = b/total
            
            # Scale the chromaticity values to 0-255 range
            r_chrom_scaled = int(r_chrom * 255)
            g_chrom_scaled = int(g_chrom * 255)
            b_chrom_scaled = int(b_chrom * 255)
            
            # Set the chromaticity values as RGB values in the new image
            chromaticity_image.putpixel((x, y), (r_chrom_scaled, g_chrom_scaled, b_chrom_scaled))
    
    return chromaticity_image

# Path to the input TIFF image
tif_path = r'C:\Users\erwan\OneDrive\Documents\GrutterLab\Data\Actual Optical Data\004_300.tif'

# Convert the TIFF image to RGB chromaticity
chromaticity_image = tif_to_rg_chromaticity(tif_path)

# Save the chromaticity image
chromaticity_image.save(r'C:\Users\erwan\OneDrive\Documents\GrutterLab\Data\Actual Optical Data\chroma_004_300.tif')
