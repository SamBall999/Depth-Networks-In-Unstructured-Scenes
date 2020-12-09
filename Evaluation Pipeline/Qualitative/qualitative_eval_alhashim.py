#Addition to DenseDepth by Alhashim et al.
#requires Tensorflow 1.13.1 
#requires Keras 2.2.4
from matplotlib import pyplot as plt

"""
Saves depth predictions as 16-bit greyscale depth maps used for quantitative evaluation.

Arguments:
- Name of model to be loaded.
- Checkpoint path to model.
- Path to images.

Returns:
- Depth map where each pixel is a 16-bit integer representing predicted depth scaled by 256.

Comments:
- Code snippet designed to be integrated into the full code for the DenseDepth network.
- Integrated into the file test.py.
"""




def display_images(outputs, inputs=None, gt=None, is_colormap=True, is_rescale=True):
    import matplotlib.pyplot as plt
    import skimage
    import cv2
    from skimage.transform import resize

    #plasma = plt.get_cmap('plasma')
    plasma = plt.get_cmap('jet')

    shape = (outputs[0].shape[0], outputs[0].shape[1], 3)
    
    all_images = []

    for i in range(outputs.shape[0]):
        imgs = []

        #print("output max")
        #print(outputs[i].max())
        #outputs[i] = outputs[i].astype(np.uint16)
        #cv2.imwrite('test2.png', outputs[i], [cv2.IMWRITE_PNG_COMPRESSION, 0])
        
        if isinstance(inputs, (list, tuple, np.ndarray)):
            x = to_multichannel(inputs[i])
            x = resize(x, shape, preserve_range=True, mode='reflect', anti_aliasing=True )
            imgs.append(x)

        if isinstance(gt, (list, tuple, np.ndarray)):
            x = to_multichannel(gt[i])
            x = resize(x, shape, preserve_range=True, mode='reflect', anti_aliasing=True )
            imgs.append(x)

        if is_colormap:
            rescaled = outputs[i][:,:,0]
            if is_rescale:
                rescaled = rescaled - np.min(rescaled)
                rescaled = rescaled / np.max(rescaled)
            imgs.append(plasma(rescaled)[:,:,:3])

            #print("rescaled output max")
            #print(rescaled.max())
            rescaled = rescaled.astype(np.uint16)
            cv2.imwrite('test3.png', rescaled, [cv2.IMWRITE_PNG_COMPRESSION, 0])
            #im = Image.fromarray(plasma(rescaled)[:,:,:3])
            #plt.save_fig(plasma(rescaled)[:,:,:3])
            #im.save(i + "_output.png")
            #print(plasma(rescaled)[:,:,:3])
            plt.figure(figsize=(10,5))
            #plt.figure(figsize=(3,5))
            #plt.imshow(rescaled, cmap="jet")
            plt.imshow(plasma(rescaled)[:,:,:3])
            plt.axis('off')
            #find image name !
            filename = "data/" + str(i) + "_output.png"
            plt.savefig(filename, bbox_inches='tight')
        else:
            imgs.append(to_multichannel(outputs[i]))

        img_set = np.hstack(imgs)
        all_images.append(img_set)

    all_images = np.stack(all_images)
    
    return skimage.util.montage(all_images, multichannel=True, fill=(0,0,0))