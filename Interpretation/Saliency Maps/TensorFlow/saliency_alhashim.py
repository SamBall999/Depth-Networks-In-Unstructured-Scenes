#Addition to DenseDepth by Alhashim et al.
#requires Tensorflow 1.13.1 
#requires Keras 2.2.4

from matplotlib import pyplot as plt
from vis.visualization import visualize_saliency
from vis.utils import utils


"""
Creates greyscale saliency map showing individual pixel contribution to the final outcome.

Arguments:
- Name of model to be loaded.
- Name of final layer of depth network.
- Path to images.

Returns:
- Saliency map of each input RGB image in the folder for use in interpretation.

Comments:
- Code snippet designed to be integrated into the full code for the DenseDepth network.
- Integrated into the file test.py.
"""

...

#load model
print('Loading model...')
model = load_model(args.model, custom_objects=custom_objects, compile=False)
print('\nModel loaded ({0}).'.format(args.model))

#input images
images = load_images( glob.glob(args.input) )
print('\nLoaded ({0}) images of size {1}.'.format(images.shape[0], images.shape[1:]))

#reshape images into format suitable for saliency function
image = images[2].reshape((1, images[2].shape[0], images[2].shape[1], images[2].shape[2]))

#perform saliency computation
layer_idx = utils.find_layer_idx(model, 'conv3') #final layer of depth network
saliency_out = visualize_saliency(model, layer_idx, None, image, backprop_modifier=None, grad_modifier="absolute") #using keras-vis library
print(saliency_out)

#plot as greyscale heat map
maximum = np.max(saliency_out) #find maximum contribution for use in rescaling
plt.imshow(saliency_out, cmap="gray", vmax = 0.4*maximum) #apply threshold to improve visualisation
plt.axis('off')
final_filename = "alhashim-saliency.png"
plt.savefig(final_filename, bbox_inches='tight') #save saliency map

...