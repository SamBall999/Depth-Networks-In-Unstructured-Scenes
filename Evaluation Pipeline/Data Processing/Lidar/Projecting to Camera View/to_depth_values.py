#SPECIAL THANKS TO DR MIKKEL KRAGH FOR HIS ASSISTANCE WITH THE LIDAR PROJECTION PROCEDURE
import numpy as np
from pypcd import pypcd
import matplotlib.pyplot as plt
from PIL import Image
from pyquaternion import Quaternion
import cv2
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import
import matplotlib.pyplot as plt


"""
Projects lidar measurements onto 2D camera view.

Arguments:
- File names of corresponding lidar PCD file and camera image.
- Static transformation between lidar scanner and left stereo camera.
- Intrinsic camera parameters.

Returns:
Projected 16-bit greyscale depth map showing projected lidar scan lines for use as ground truth.
"""

# Initialization
img_size = [544, 1024]

pic_filename = '1477388576.197643000.png'
lidar_filename = 'm_1477388576.441035000.pcd'

# Extrinsic parameters from ROS
Trans_cam_li = [-0.063, 0.436, -0.318, 1]
q = Quaternion(-0.444, 0.568, -0.547, 0.425)
Rot_mat_4d = q.transformation_matrix

# Intrinsic camera matrix from ROS
Intrinsic_Matrix = np.array([[580.6427001953125, 0.0, 512.0, 0.0], [0.0, 580.6427001953125, 254.5, 0.0], [0.0, 0.0, 1.0, 0.0]])

# Load point cloud data
#pc = pypcd.PointCloud.from_path('m_1477388636.304054000.pcd')
pc = pypcd.PointCloud.from_path(lidar_filename)
x = pc.pc_data['x']
y = pc.pc_data['y']
z = pc.pc_data['z']

# Convert to homogenous coordinates
homogenous = np.ones_like(z)
xyz_h = np.stack([x,y,z,homogenous])

# Construct Transformation Matrix (extrinsic, intrinsic)
Trans_mat_4d = np.eye(4)
Trans_mat_4d[:,3] = Trans_cam_li
Extrinsic_matrix = np.linalg.inv(Trans_mat_4d @ Rot_mat_4d)
Projection = np.asarray([[1,0,0,0],
                        [0,1,0,0],
                        [0,0,1,0]])
P = Intrinsic_Matrix @ Extrinsic_matrix

# Transform points
pixel_3d = np.dot(P, xyz_h)
xyz_h_cam = Extrinsic_matrix @ xyz_h

# Remove 3D points that are behind the camera
remove_inds = pixel_3d[2,:] < 0
pixel_3d = pixel_3d[:,np.logical_not(remove_inds)]
xyz_h_cam = xyz_h_cam[:,np.logical_not(remove_inds)]
point2d = pixel_3d / pixel_3d[2,:] # Can also be done using 'Projection' matrix above
norm3d_rounded = np.rint(np.array(point2d))

# Remove 3D points that (when projected) are outside the image
remove_inds = np.any([norm3d_rounded[0,:] < 0,norm3d_rounded[0,:] >= img_size[1], norm3d_rounded[1,:] < 0,norm3d_rounded[1,:] >= img_size[0]], axis=0)
norm3d_rounded = norm3d_rounded[:,np.logical_not(remove_inds)]
xyz_h_cam = xyz_h_cam[:,np.logical_not(remove_inds)]

print(norm3d_rounded.shape)
print(xyz_h_cam.shape)

print(xyz_h_cam[2,1])

# Load image
#img_pil = Image.open('1477388065.774615000.jpg')
img_pil = Image.open(pic_filename)
img = np.array(img_pil)

#blank_img_pil = Image.new('RGB', (1024,544), (0,0,0))
#blank_img = np.array(blank_img_pil)
blank_img = np.zeros((544,1024), dtype=np.uint16)

from colorsys import hsv_to_rgb

def pseudocolor(val, minval, maxval):
    """ Convert val in range minval..maxval to the range 0..120 degrees which
        correspond to the colors Red and Green in the HSV colorspace.
    """
    print(val) #is val the depth value??
    h = (float(val-minval) / (maxval-minval)) * 120

    # Convert hsv color (h,1,1) to its rgb equivalent.
    # Note: hsv_to_rgb() function expects h to be in the range 0..1 not 0..360
    r, g, b = hsv_to_rgb(h/360, 1., 1.)
    return r, g, b
min_depth = 0#np.min(xyz_h_cam[2,:])
max_depth = 30#np.max(xyz_h_cam[2,:])

max_est_depth = 0
min_est_depth = 50
# Plot the image and draw projected 3D point on top
for i in range(norm3d_rounded.shape[1]):
    [x0, y0, _] = norm3d_rounded[:,i]
    #img[int(y0),int(x0),:] = np.asarray(pseudocolor(xyz_h_cam[2,i],min_depth,max_depth))*255
    #blank_img[int(y0),int(x0),:] = np.asarray(pseudocolor(xyz_h_cam[2,i],min_depth,max_depth))*255
    print(np.asarray(xyz_h_cam[2,i])*256) 
    blank_img[int(y0),int(x0)] = np.asarray(xyz_h_cam[2,i])*256 #convert to 16 bit depth
    if (xyz_h_cam[2,i] > max_est_depth):
        max_est_depth = xyz_h_cam[2,i]
    if (xyz_h_cam[2,i] < min_est_depth):
        min_est_depth = xyz_h_cam[2,i]
    #by using the format you have saved it in - can just divide by x to get original depth values back

#plt.imshow(img)
print(max_est_depth)
print(min_est_depth)
print(np.max(blank_img))
blank_16 = blank_img.astype(np.uint16)
print(np.max(blank_16))
plt.imshow(blank_img)
plt.axis('off')
final_filename = filename + "-projected.png"
plt.savefig(final_filename, bbox_inches='tight', dpi = 300)
cv2.imwrite( 'output16.png', blank_16) 
plt.show()