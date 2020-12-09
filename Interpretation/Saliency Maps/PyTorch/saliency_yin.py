#Addition to VNL by Yin et al.  
#PyTorch 
from matplotlib import pyplot as plt
import cv2

"""
Creates greyscale saliency map showing individual pixel contribution to the final outcome.

Arguments:
- Name of model to be loaded.
- Checkpoint path to model.
- Path to images.

Returns:
- Saliency map of each input RGB image in the folder for use in interpretation.

Comments:
- Code snippet designed to be integrated into the full code for the VNL network.
- Integrated into the file test_any_images.py.
"""

...   

#create data loader
data_loader = CustomerDataLoader(test_args)
test_datasize = len(data_loader)
logger.info('{:>15}: {:<30}'.format('test_data_size', test_datasize))

#load model
model = MetricDepthModel()
model.eval()

#load checkpoint
if test_args.load_ckpt:
    load_ckpt(test_args, model)
model.cuda()
model = torch.nn.DataParallel(model)



#load input images
path = "./datasets/Lychees" #define image data path
img = cv2.imread(os.path.join(path, i))
#img_resize = cv2.resize(img, (int(img.shape[1]), int(img.shape[0])), interpolation=cv2.INTER_LINEAR)
img_resize = cv2.resize(img, (int(img.shape[1]*0.6), int(img.shape[0]*0.6)), interpolation=cv2.INTER_LINEAR)
img_torch1 = scale_torch(img_resize, 255)
img_torch = img_torch1[None, :, :, :].cuda()

img_torch.requires_grad_()

#perform depth prediction forward pass
_, pred_depth_softmax= model.module.depth_model(img_torch)
pred_depth = bins_to_depth(pred_depth_softmax)
#pred_depth = pred_depth.cpu().numpy().squeeze()
pred_depth = pred_depth.cpu().detach().numpy().squeeze()

#get saliency map
pred_depth_softmax = pred_depth_softmax.sum()  #sum of each depth prediction in the image
img_torch.retain_grad() #enable gradient
pred_depth_softmax.backward() #perform backward pass to find gradient of depth prediction sum w.r.t input image
saliency, _ = torch.max(img_torch.grad.data.abs(),dim=1) #get maximum saliency contribution across the three RGB channels for each pixel

final_saliency = saliency.cpu()

#find maximum for use in rescaling
maximum = final_saliency[0].max()
print(maximum)

#code to plot the saliency map as a heatmap
plt.imshow(final_saliency[0], cmap="gray", vmax = maximum*0.4) #apply threshold to improve visualisation
#plt.imshow(final_saliency[0], cmap="gray", vmax = 5e-07)
plt.axis('off')
final_filename = "results/" + i + "-yin-saliency.png"
plt.savefig(final_filename, bbox_inches='tight') #save saliency map


...