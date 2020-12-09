import os

"""
Creates text file containing file names for each image in the folder.
For use with the BTS network.

Arguments:
- Folder name of target input images.
- Focal length of camera used to collect image data.

Returns:
- Textfile containing filenames of each image along with focal length of relevant camera.
"""

#set parameters
folder = "./lychee_subset/" #folder name containing input RGB images
focal_length = '404.472' #focal length of relevant camera


file1 = open("MyFile.txt","a")

for filename in sorted(os.listdir(folder)): #sort filenames by number
    print(filename)
    if(filename == ".DS_Store"): #skip
        continue
    #write in format specified for BTS network
    file1.write(filename)
    file1.write(" ")
    file1.write(filename)
    file1.write(" ")
    file1.write(focal_length)
    file1.write("\n")


file1.close()