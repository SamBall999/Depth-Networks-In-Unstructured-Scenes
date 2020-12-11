%Script to convert ROS image messages to png format
%Implemented using MATLAB R2020a and MATLAB ROS Toolbox

bag = rosbag("2016-10-25-11-41-21_example.bag"); %create rosbag object
bagselect1 = select(bag, 'Topic', '/Multisense/left/image_rect_color') %select topic containing left stereo images
msgs= readMessages(bagselect1, 1:100); %select 100 messages at a time due to memory constraints
for j=1:100  %for each image message
    I = readImage(msgs{j}); %read in image
    sec = int2str(msgs{j}.Header.Stamp.Sec); %get timestamp seconds
    nsec = int2str(msgs{j}.Header.Stamp.Nsec); %get timestamp nanoseconds
    s = strcat(sec,'.',nsec,'.png'); %create filename
    imwrite(I, s) %save as png
end

