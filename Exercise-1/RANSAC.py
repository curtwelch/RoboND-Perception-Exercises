#!/usr/bin/python

# Import PCL module
import pcl

# Load Point Cloud file
cloud = pcl.load_XYZRGB('tabletop.pcd')

# Voxel Grid filter
# Create a VoxelGrid filter object for our input point cloud
vox = cloud.make_voxel_grid_filter()

# Choose a voxel (also known as leaf) size
# Note: this (1) is a poor choice of leaf size   
# Experiment and find the appropriate size!
LEAF_SIZE = 0.005   

# Set the voxel (or leaf) size  
vox.set_leaf_size(LEAF_SIZE, LEAF_SIZE, LEAF_SIZE)

# Call the filter function to obtain the resultant downsampled point cloud
cloud_filtered = vox.filter()
# filename = 'v%dmm.pcd' % (int(LEAF_SIZE*1000),)
# print "file name is", filename
filename = 'voxel_downsampled.pcd'
pcl.save(cloud_filtered, filename)

##################################################
# PassThrough filter
# Remove everytig below table
##################################################
# Create a PassThrough filter object.
passthrough = cloud_filtered.make_passthrough_filter()

# Assign axis and range to the passthrough filter object.
filter_axis = 'z'
passthrough.set_filter_field_name (filter_axis)
axis_min = .76
axis_max = 1.2
passthrough.set_filter_limits (axis_min, axis_max)

# Finally use the filter function to obtain the resultant point cloud. 
cloud_filtered = passthrough.filter()
print "filtered on z now has size:", cloud_filtered.size
filename = 'pass_through_filtered.pcd'
pcl.save(cloud_filtered, filename)

##################################################
# PassThrough filter
# Remove front edge of table
##################################################
# Create a PassThrough filter object.
passthrough = cloud_filtered.make_passthrough_filter()

# Assign axis and range to the passthrough filter object.
filter_axis = 'y'
passthrough.set_filter_field_name (filter_axis)
axis_min = -3
axis_max = -1.35
passthrough.set_filter_limits (axis_min, axis_max)

# Finally use the filter function to obtain the resultant point cloud. 
cloud_filtered = passthrough.filter()
print "filtered on y now has size:", cloud_filtered.size
filename = 'pass_through_filtered2.pcd'
pcl.save(cloud_filtered, filename)

##################################################
# RANSAC plane segmentation
# Create the segmentation object
##################################################
seg = cloud_filtered.make_segmenter()

# Set the model you wish to fit 
seg.set_model_type(pcl.SACMODEL_PLANE)
seg.set_method_type(pcl.SAC_RANSAC)

# Max distance for a point to be considered fitting the model
# Experiment with different values for max_distance 
# for segmenting the table

max_distance = 0.01
seg.set_distance_threshold(max_distance)

# Call the segment function to obtain set of inlier indices and model coefficients
inliers, coefficients = seg.segment()
# print len(inliers), len(coefficients)

# Extract inliers
extracted_inliers = cloud_filtered.extract(inliers, negative=False)

# Save pcd for table
filename = 'extracted_inliers.pcd'
pcl.save(extracted_inliers, filename)

# Extract outliers
extracted_outliers = cloud_filtered.extract(inliers, negative=True)
print "objects clould size:", extracted_outliers.size

# Save pcd for tabletop objects
filename = 'extracted_outliers.pcd'
pcl.save(extracted_outliers, filename)

print "objects clould size after save:", extracted_outliers.size

if 0:
    # Failed!  Front edge wasn't as laege as object tops!

    ##################################################
    # Try it again to pick out the front edge of the table!
    # RANSAC plane segmentation
    # Create the segmentation object
    ##################################################
    seg2 = extracted_outliers.make_segmenter()

    # Set the model you wish to fit 
    seg2.set_model_type(pcl.SACMODEL_PLANE)
    seg2.set_method_type(pcl.SAC_RANSAC)

    # Max distance for a point to be considered fitting the model
    # Experiment with different values for max_distance 
    # for segmenting the table

    max_distance = 0.01
    seg2.set_distance_threshold(max_distance)

    # Call the segment function to obtain set of inlier indices and model coefficients
    inliers2, coefficients = seg2.segment()
    # print len(inliers2), len(coefficients)

    # Extract inliers
    extracted_inliers2 = extracted_outliers.extract(inliers2, negative=False)

    # Save pcd for table
    filename = 'extracted_inliers2.pcd'
    pcl.save(extracted_inliers2, filename)

    # Extract outliers
    extracted_outliers2 = extracted_outliers.extract(inliers2, negative=True)

    # Save pcd for tabletop objects
    filename = 'extracted_outliers2.pcd'
    pcl.save(extracted_outliers2, filename)

