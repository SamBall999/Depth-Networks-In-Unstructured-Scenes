%Script to read in PCD files and save in corrected PCD format to ensure compatibility with next stage of processing.
%Implemented in MATLAB R2020a using the MATLAB Computer Vision Toolbox.
%Used to correct incompatibility with certain fields in the PCD format.

myDir = "Lidar";	%access files extracted from ros bag
myFiles = dir(fullfile(myDir,'*.pcd'));	%read in all names of pcd files
fprintf('Length of files %d \n', length(myFiles)) %print number of files
for k = 1:length(myFiles) %for each pcd file
	baseFileName = myFiles(k).name; %get filename
	fullFileName = fullfile(myDir, baseFileName); %get relative file path
	fprintf(1, 'Now reading %s\n', baseFileName);
    	ptCloud = pcread(fullFileName); %read in as pointcloud
    	new_filename = strcat('Lidar_pcd_matlab/m_', baseFileName); %move to new folder
    	pcwrite(ptCloud, new_filename); %save in .pcd format to ensure compatibility with pypcd library
end



