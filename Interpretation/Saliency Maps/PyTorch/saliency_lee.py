#Addition to BTS by Lee et al.  
#PyTorch 
from matplotlib import pyplot as plt

"""
Creates greyscale saliency map showing individual pixel contribution to the final outcome.

Arguments:
- Name of model to be loaded.
- Checkpoint path to model.
- Path to images.

Returns:
- Saliency map of each input RGB image in the folder for use in interpretation.

Comments:
- Code snippet designed to be integrated into the full code for the BTS network.
- Integrated into the file bts_test.py in the test function.
"""

...   

#load data
args.mode = 'test'
dataloader = BtsDataLoader(args, 'test') 

#load model
model = BtsModel(params=args)
model = torch.nn.DataParallel(model)  
checkpoint = torch.load(args.checkpoint_path)
model.load_state_dict(checkpoint['model'])
model.eval()
model.cuda()

num_test_samples = get_num_lines(args.filenames_file)

with open(args.filenames_file) as f:
    lines = f.readlines()

print('now testing {} files with {}'.format(num_test_samples, args.checkpoint_path))
   
#create arrays to hold depth predictions and intermediate results of Local Planar Guidance (LPG) layers
pred_depths = []
pred_8x8s = []
pred_4x4s = []
pred_2x2s = []
pred_1x1s = []  
   

#iterate through input images and create saliency map for each   
i=0
for _, sample in enumerate(tqdm(dataloader.data)):
    
    #define input variables
    image = Variable(sample['image'].cuda())
    image.requires_grad = True #enable gradient for input image
    focal = Variable(sample['focal'].cuda())

    #perform depth prediction forward pass
    lpg8x8, lpg4x4, lpg2x2, reduc1x1, depth_est = model(image, focal) 
    #save depth predictions
    pred_depths.append(depth_est.cpu().detach().numpy().squeeze())
    #save output of LPG layers at different scales
    pred_8x8s.append(lpg8x8[0].cpu().detach().numpy().squeeze())
    pred_4x4s.append(lpg4x4[0].cpu().detach().numpy().squeeze())
    pred_2x2s.append(lpg2x2[0].cpu().detach().numpy().squeeze())
    pred_1x1s.append(reduc1x1[0].cpu().detach().numpy().squeeze())


    #get saliency map
    depth_est = depth_est.sum() #sum of each depth prediction in the image
    image.retain_grad() #enable gradient
    depth_est.backward() #perform backward pass to find gradient of depth prediction sum w.r.t input image
    saliency, _ = torch.max(image.grad.data.abs(),dim=1) #get maximum saliency contribution across the three RGB channels for each pixel

    final_saliency = saliency.cpu() 

    #find maximum for use in rescaling
    maximum = final_saliency[0].max() 
    print(maximum)

    #code to plot the saliency map as a heatmap
    plt.imshow(final_saliency[0], cmap="gray", vmax = 0.40*maximum) #apply threshold to improve visualisation
    plt.axis('off')
    final_filename = "results/" + str(i) + "-lee-saliency.png"
    plt.savefig(final_filename, bbox_inches='tight')  #save saliency map
    i += 1

...