
import matplotlib.pyplot as plt
import skimage
import os
from skimage.transform import resize
import matplotlib.image as mpimg

"""
Converts 16-bit greyscale depth maps to jet colourmaps.

Arguments:
Folder name of target 16-bit depth maps.

Returns:
Colour map of each 16-bit depth map in the folder for visualisation.
"""

folder = "./final/" #folder name containing 16-bit depth maps

for filename in os.listdir(folder):
    print(filename)
    if(filename == ".DS_Store"): #to ensure continuous processing 
        continue
    img = mpimg.imread(os.path.join(folder, filename))
    plt.imshow(img, cmap="jet") #plot as jet colour map

    plt.axis('off') #remove axes
    final_filename = filename + "-colour.png"
    plt.savefig(final_filename, bbox_inches='tight') #save without surrounding whitespace

