#Addition to VNL by Yin et al.  
#PyTorch 
from matplotlib import pyplot as plt
import cv2

"""
Saves depth predictions as 16-bit greyscale depth maps used for quantitative evaluation.

Arguments:
- Name of model to be loaded.
- Checkpoint path to model.
- Path to images.

Returns:
- Depth map where each pixel is a 16-bit integer representing predicted depth scaled by 256.

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


#define input and output paths
path = "./datasets/Lychees"
resultspath = "./Lychee_results/"
imgs_list = os.listdir(path)

#find depth prediction output for each image
for i in imgs_list:
    print("image name ")
    if(i==".DS_Store"): #skip
        continue
    print(i)
    with torch.no_grad():

        #load input images
        img = cv2.imread(os.path.join(path, i))
        img_resize = cv2.resize(img, (int(img.shape[1]), int(img.shape[0])), interpolation=cv2.INTER_LINEAR)
        img_torch1 = scale_torch(img_resize, 255)
        img_torch = img_torch1[None, :, :, :].cuda()
        
        #perform depth prediction 
        _, pred_depth_softmax= model.module.depth_model(img_torch)
        pred_depth = bins_to_depth(pred_depth_softmax)
        pred_depth = pred_depth.cpu().numpy().squeeze()

        #scale according to maximum depth
        pred_depth_100 = pred_depth*100 #fieldsafe and ACFR max depth
        #pred_depth_100 = pred_depth*80 #kitti max depth
        print(pred_depth_100.max())
        print(pred_depth_100.min())
        #pred_depth_scale = (pred_depth / pred_depth.max() * 60000).astype(np.uint16)  # scale 60000 for visualization
        pred_depth_scale = (pred_depth_100 * 256).astype(np.uint16)  #multiply by 256 and convert to 16-bit int

        cv2.imwrite(os.path.join(resultspath, i), pred_depth_scale) #save as 16-bit depth map

...