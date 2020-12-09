#Addition to BTS by Lee et al.  
#PyTorch 
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


start_time = time.time()
    with torch.no_grad():
        for _, sample in enumerate(tqdm(dataloader.data)):
            image = Variable(sample['image'].cuda())
            focal = Variable(sample['focal'].cuda())
            # Predict
            lpg8x8, lpg4x4, lpg2x2, reduc1x1, depth_est = model(image, focal)
            pred_depths.append(depth_est.cpu().numpy().squeeze())
            pred_8x8s.append(lpg8x8[0].cpu().numpy().squeeze())
            pred_4x4s.append(lpg4x4[0].cpu().numpy().squeeze())
            pred_2x2s.append(lpg2x2[0].cpu().numpy().squeeze())
            pred_1x1s.append(reduc1x1[0].cpu().numpy().squeeze())

elapsed_time = time.time() - start_time
print('Elapesed time: %s' % str(elapsed_time))
print('Done.')


for s in tqdm(range(num_test_samples)):

...

        pred_depth = pred_depths[s]
        pred_8x8 = pred_8x8s[s]
        pred_4x4 = pred_4x4s[s]
        pred_2x2 = pred_2x2s[s]
        pred_1x1 = pred_1x1s[s]
        
        if args.dataset == 'kitti' or args.dataset == 'kitti_benchmark':
            pred_depth_scaled = pred_depth * 256.0
            print(pred_depth_scaled.max())
            print(pred_depth_scaled.min())
        else:
            pred_depth_scaled = pred_depth * 1000.0
        
        pred_depth_scaled = pred_depth_scaled.astype(np.uint16)
        cv2.imwrite(filename_pred_png, pred_depth_scaled, [cv2.IMWRITE_PNG_COMPRESSION, 0])


...