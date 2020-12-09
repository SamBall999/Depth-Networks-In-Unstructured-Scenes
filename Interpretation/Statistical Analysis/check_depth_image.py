from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

"""
Compare ranges and distribution of depth predictions for each network against the ground truth range.

Inputs:
File names of each 16-bit depth maps and corresponding ground truth file.

Returns:
Violin plot comparing distributions of predicted depths and individual distribution plots for each network.
"""


def set_axis_style(ax, labels):
    ax.get_xaxis().set_tick_params(direction='out')
    ax.xaxis.set_ticks_position('bottom')
    ax.set_xticks(np.arange(1, len(labels) + 1))
    ax.set_xticklabels(labels)
    ax.set_xlim(0.25, len(labels) + 0.75)
    ax.set_xlabel('Network')


#input depth maps from each network
filename_1 = "1477388606.399309000-a.png" #depth map filename from DenseDepth network by Alhashim et al.
filename_2 = "1477388606.399309000-l.png" #depth map filename from BTS network by Lee et al.
filename_3 = "1477388606.399309000-y.png" #depth map filename from VNL network by Yin et al.
filename_4 = "m1477388606.420140000.pcd-gt.png" #corresponding groundtruth filename

#open each depth map as a numpy array
depth_png_1 = np.array(Image.open(filename_1), dtype=int)
depth_png_2 = np.array(Image.open(filename_2), dtype=int)
depth_png_3 = np.array(Image.open(filename_3), dtype=int)
depth_gt = np.array(Image.open(filename_4), dtype=int)
#assert(np.max(depth_png) > 255)

#recover actual depth quantities
depth_1 = depth_png_1.astype(np.float) / 256
depth_2 = depth_png_2.astype(np.float) / 256
depth_3 = depth_png_3.astype(np.float) / 256
depth_gt = depth_gt.astype(np.float) / 256

print(np.median(depth_1[np.nonzero(depth_1)]))
print(np.mean(depth_1[np.nonzero(depth_1)]))

depth_1[depth_png_1 == 0] = -1
#depth_gt[depth_gt == 0] = -1

print(np.max(depth_1))
print(np.min(depth_1))
print(np.min(depth_1[depth_1 != -1]))

gt_max = np.max(depth_gt)
gt_min = np.min(depth_gt[depth_gt != 0])
max_array = np.full(1000000, gt_max)
min_array = np.full(1000000, gt_min)
depth_range = np.concatenate((max_array, min_array))

depth_2 = depth_2[depth_2 < 69]



#create plots

###PLOT ONE: Violin plot comparing depth ranges###
data_to_plot = [depth_1[depth_1 != -1], depth_2[depth_2 != -1], depth_3[depth_3 != -1], depth_gt[depth_gt != 0]]  #combine different distributions into a list
fig = plt.figure() #create a figure instance
ax = fig.add_subplot(111) #create an axes instance
ax.set_ylabel('Depth')
labels = ['Alhashim', 'Lee', 'Yin', 'Ground Truth']
set_axis_style(ax, labels)

###PLOT TWO: Box plot comparing depth ranges###
bp = ax.violinplot(data_to_plot)
plt.ylim(0, 70)
for pc in bp['bodies']:
    #pc.set_facecolor('#F1BBA3')
    pc.set_facecolor('#F1CCBE') #most recent
    #pc.set_edgecolor('#F19B94')
    #pc.set_facecolor('#C5E0B4')
    pc.set_alpha(1)
# Make all the violin statistics marks red:
for partname in ('cbars','cmins','cmaxes'):
    vp = bp[partname]
    #vp.set_edgecolor('#F78D7A') 
    vp.set_edgecolor('#F19B94')
    #vp.set_edgecolor('#87C183')
    vp.set_linewidth(1.5)
plt.show()

fig_1 = plt.figure() # Create a figure instance
ax_1 = fig_1.add_subplot(111) # Create an axes instance
#ax = fig.add_axes([0,0,1])
ax_1.set_ylabel('Depth')
#labels = ['DenseDepth', 'BTS', 'VNL']
labels = ['Alhashim', 'Lee', 'Yin']
set_axis_style(ax_1, labels)
# Create the boxplot
bp_1 = ax_1.boxplot(data_to_plot)
plt.show()


###PLOT THREE: Depth prediction distribution for DensDepth network###
np.random.seed(0)
ax_2 = sns.distplot(depth_1[depth_1 != -1], color = "#F19B94") #color="#FFCE9F"
#ax_2 = sns.distplot(depth_1[depth_1 != -1], color = "#9FC687") #color="#FFCE9F"
ax_2.set_xlabel('Depth Value')
ax_2.set_ylabel('Frequency')
plt.xlim(0, 70)
plt.show()


###PLOT FOUR: Depth prediction distribution for BTS network###
np.random.seed(0)
ax_3 = sns.distplot(depth_2[depth_2 != -1],  color = "#F19B94") #color="#FFCE9F" #FFC2A1
ax_3.set_xlabel('Depth Value')
ax_3.set_ylabel('Frequency')
plt.xlim(0, 70)
plt.show()


###PLOT FIVE: Depth prediction distribution for VNL network###
np.random.seed(0)
ax_4 = sns.distplot(depth_3[depth_3 != -1],  color = "#F19B94") #color="#FFCE9F"
ax_4.set_xlabel('Depth Value')
ax_4.set_ylabel('Frequency')
plt.xlim(0, 70)
plt.show()

###PLOT SIX: Groundtruth depth distribution###
np.random.seed(0)
ax_5 = sns.distplot(depth_gt[depth_gt != 0], color = "#F19B94") #color="#FFCE9F"
ax_5.set_xlabel('Depth Value')
ax_5.set_ylabel('Frequency')
plt.xlim(0, 60)
plt.show()

