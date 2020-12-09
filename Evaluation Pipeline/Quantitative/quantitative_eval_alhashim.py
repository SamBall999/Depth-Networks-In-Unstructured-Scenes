#Addition to DenseDepth by Alhashim et al.
#requires Tensorflow 1.13.1 
#requires Keras 2.2.4
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
- Code snippet designed to be integrated into the full code for the DenseDepth network.
- Integrated into the file test.py.
"""

...   

# Compute results
outputs = scale_up(2, predict_custom(model, inputs))

print("outside predictions max")
print(outputs[0].max())

print("outside predictions min")
print(outputs[0].min())

resultspath = "acfr_final_results/"

for i in range(outputs.shape[0]):
      pred_depth = outputs[i]
      pred_depth_100 = pred_depth*100
      print(pred_depth_100.max())
      print(pred_depth_100.min())
      pred_depth_scale = (pred_depth_100 * 256).astype(np.uint16)
      cv2.imwrite(os.path.join(resultspath, str(i) + '-new.png'), pred_depth_scale) 

...