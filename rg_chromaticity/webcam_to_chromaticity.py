import cv2
import numpy as np

def display_input():    #test function to ensure the image is being pulled from the webcam correctly
    while True:
        ret, frame = cam.read()     #ret: boolean indicating whether image is grabbed correctly, frame: image being read
        
        #if no frame is grabbed, throw an error message
        if not ret:
            print("failed to grab frame")
            break
        
        #if there is a frame, display it
        try:
            cv2.imshow("Camera", frame)

        #error message in case of error
        except Exception as e:
            print(f'Error grabbing frame: {e}')

        #assign to k the value of the first key pressed (while cv2 is in focus)
        k = cv2.waitKey(1)
        if k%256 == 27:     #checks whether escape is pressed
            try:
                print("Escape hit, closing...")
                break
            except Exception as e:
                print(f'Error exiting the program: {e}')

\
#actual funciton, converts an IMAGE to chromaticity
def to_chromaticity(image_in):
    try:
        #TODO ensure RGB input

        # Convert the image to numpy array
        rgb_array = np.array(image_in)

        # Calculate chromaticity values
        total = np.sum(rgb_array, axis=2)
        total[total == 0] = 1  # Avoid division by zero

        #divide each count by the total of values at this pixel
        r_chrom = rgb_array[:, :, 0] / total
        g_chrom = rgb_array[:, :, 1] / total
        b_chrom = 1 - r_chrom - g_chrom

        # Scale the chromaticity values to 0-255 range
        r_chrom_scaled = (r_chrom * 255).astype(np.uint8)
        g_chrom_scaled = (g_chrom * 255).astype(np.uint8)
        b_chrom_scaled = (b_chrom * 255).astype(np.uint8)

        # Combine the channels into a new image in BGR format, which seems to be required by cv2
        chroma_array = np.stack((b_chrom_scaled, g_chrom_scaled, r_chrom_scaled), axis=2)

        #TODO subtract an array of the chosen values here

        #make this into an image
        chroma_image = cv2.cvtColor(chroma_array, cv2.COLOR_RGB2BGR)

        return chroma_image

    except Exception as e: 
       print(f'Error converting to chromaticity: {e}')


#open camera
try:
    global cam
    cam = cv2.VideoCapture(0)

except Exception as e:
    print(f'Error opening camera: {e}')

#TODO: set exposure. The way it is done here may or may not work
#cam.set(cv2.CAP_PROP_EXPOSURE, 80) 

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
    if cv2.waitKey(1)%256 == 27:
        try:
            print("Escape hit, closing...")
            break
        except Exception as e:
            print(f'Error exiting the loop:{e}')
    
    #TODO: take a picture of original and modified feed. commented out because this is stolen from stack overflow and may or may onot work with the current implementation of the code
    # #check for space key to take a picture
    # elif k%256 == 32:     
    #     # SPACE pressed
    #     img_name = "opencv_frame_{}.png".format(img_counter)
    #     cv2.imwrite(img_name, frame)
    #     print("{} written!".format(img_name))
    #     img_counter += 1



#release resources
cam.release()
cv2.destroyAllWindows()