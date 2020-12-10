## Extracting FieldSafe Image Data

The FieldSAFE dataset utilised ROS (Robot Operating System) to record the sensor
data, publishing all sensor data in the form of rosbags. 

To extract the image data into png format, the MATLAB R2020 ROS Toolbox was utilised as follows:

- The RGB images from the left stereo camera were extracted from the uncompressed sensor msgs/Image message format and saved to png format for use as the depth network input.

- The messages were read in and saved to png format in batches of 100 due to memory
constraints.