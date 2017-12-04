import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

# Read in the image
# There are six more images available for reading
# called sample1-6.jpg, feel free to experiment with the others!
image_name = '../calibration_images/example_rock2.jpg'
image = mpimg.imread(image_name)

# Define a function to perform a color threshold
def color_thresh(img, rgb_thresh=(0, 0, 0)):
    ###### TODO:
    # Create an empty array the same size in x and y as the image 
    # but just a single channel
    color_select = np.zeros_like(img[:,:,0])
    # Apply the thresholds for RGB and assign 1's 
    # where threshold was exceeded
    # Return the single-channel binary image
    above_thresh = (img[:,:,0] > rgb_thresh[0]) & (img[:,:,1] > rgb_thresh[1]) & (img[:,:,2] > rgb_thresh[2])
    
    color_select[above_thresh] = 1
    return color_select

def color_thresh_range(img, rgb_thresh_low=(0, 0, 0), rgb_thresh_high=(255, 255, 255)):
    ###### TODO:
    # Create an empty array the same size in x and y as the image 
    # but just a single channel
    color_select = np.zeros_like(img[:,:,0])
    # Apply the thresholds for RGB and assign 1's 
    # where threshold was exceeded
    # Return the single-channel binary image
    above_thresh = (img[:,:,0] < rgb_thresh_low[0]) | (img[:,:,1] < rgb_thresh_low[1]) | (img[:,:,2] < rgb_thresh_low[2]) | (img[:,:,0] > rgb_thresh_high[0]) | (img[:,:,1] > rgb_thresh_high[1]) | (img[:,:,2] > rgb_thresh_high[2])
    
    color_select[above_thresh] = 1
    return color_select
    
# Define color selection criteria
###### TODO: MODIFY THESE VARIABLES TO MAKE YOUR COLOR SELECTION
red_threshold = 140
green_threshold = 110
blue_threshold = 5
######
rgb_threshold_low = (130, 110, 0)
rgb_threshold_high = (210, 180, 40)

# pixels below the thresholds
colorsel = color_thresh_range(image, rgb_thresh_low=rgb_threshold_low, rgb_thresh_high=rgb_threshold_high)

# Display the original image and binary               
f, (ax1, ax2) = plt.subplots(1, 2, figsize=(21, 7), sharey=True)
f.tight_layout()
ax1.imshow(image)
ax1.set_title('Original Image', fontsize=40)

ax2.imshow(colorsel, cmap='gray')
ax2.set_title('Your Result', fontsize=40)
plt.subplots_adjust(left=0., right=1, top=0.9, bottom=0.)
plt.show() # Uncomment if running on your local machine