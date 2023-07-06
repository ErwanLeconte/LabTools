import cv2
import numpy as np

def display_input():
    while True:
        ret, frame = cam.read()
        if not ret:
            print("failed to grab frame")
            break
        try:
            cv2.imshow("Camera", frame)
        except Exception as e:
            print(f'Error grabbing frame: {e}')

        k = cv2.waitKey(1)
        if k%256 == 27:
            try:
                # ESC pressed
                print("Escape hit, closing...")
                break
            except Exception as e:
                print(f'Error exiting the program: {e}')

def to_chromaticity(image_in):
    try:
        #TODO ensure RGB input

        # Convert the image to numpy array
        rgb_array = np.array(image_in)

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

        # Combine the channels into a new image in BGR format, which seems to be required by cv2
        chroma_array = np.stack((b_chrom_scaled, g_chrom_scaled, r_chrom_scaled), axis=2)
        chroma_image = cv2.cvtColor(chroma_array, cv2.COLOR_RGB2BGR)

        return chroma_image

    except Exception as e: 
       print(f'Error converting to chromaticity: {e}')

#variables

#open camera
try:
    global cam
    cam = cv2.VideoCapture(0)

except Exception as e:
    print(f'Error opening camera: {e}')

#TODO: set exposure
cam.set(cv2.CAP_PROP_EXPOSURE, -10
        ) 

#create a window to display the result
cv2.namedWindow('output')

#main loop
while(True):
    #grab the current frame
    ret, frame = cam.read()
    if not ret:
        print("failed to grab frame")
        break

    #process the frame
    chroma_frame = to_chromaticity(frame)

    #display the frame
    cv2.imshow('output', chroma_frame)
    cv2.waitKey(1)
    #check for escape -> exit the loop
    # k =   #variable for key pressed when cv2 is in focus
    if cv2.waitKey(1)%256 == 27:
        try:
            print("Escape hit, closing...")
            break
        except Exception as e:
            print(f'Error exiting the loop:{e}')
    
    #TODO: take a picture of original and modified feed
    # #check for space to take a picture
    # elif k%256 == 32:     
    #     # SPACE pressed
    #     img_name = "opencv_frame_{}.png".format(img_counter)
    #     cv2.imwrite(img_name, frame)
    #     print("{} written!".format(img_name))
    #     img_counter += 1



#release resources
cam.release()
cv2.destroyAllWindows()