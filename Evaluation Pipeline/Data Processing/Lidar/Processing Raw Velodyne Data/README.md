## Processing Raw Velodyne Data

#### Install ROS Melodic on Ubuntu 18.04

#### Install velodyne library. 

Check your installation as follows:

```
    rospack find velodyne_pointcloud
````


#### Convert from velodyne_packets (velodyne_msgs/VelodyneScan) to velodyne_points (PointCloud2)

In four separate terminals, run, in order:

```
    roscore
````

```
    rosrun nodelet nodelet standalone velodyne_pointcloud/CloudNodelet _model:=32E _calibration:=/opt/ros/melodic/share/velodyne_pointcloud/params/32db.yaml
````

```
    rosrun rosbag record -O pointcloud3.bag /velodyne_points
````

```
    rosbag play file.bag
````


#### Check subscriber and publishers nodes are correct as follows: 

```
    rostopic info /velodyne_points
````