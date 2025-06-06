# Image Processing Pipeline

## Purpose
Meant to standardize image datasets for use with object recognition models. Many models are meant to be used with a specific resolution or simply have their results significantly impacted by the resolution of images. This pipeline standardizes the resolution and aspect ratio of each image.

### Parser.py <directoryPath>
First step is to run the parser script. It will search any directory for images, and store metadata relating to filename, file path, height, width, and total pixel count. This data will be stored in a singular csv named ImageResolutions.

### Partitioner.py <ImageResolutions.csv> <#ofParts>
Second step is to run the partitioner script. It runs an algorithm to figure out where to partition the given dataset, but with an unusual approach. Images often are a variety of resolutions, there are plenty of outliers, images of super low resolution, and super high resolution. To account for these outliers you have to take a nuanced approach, by avoiding the use of the resolution when partitioning and simply grabbing records directly. The process includes, first taking input on how many parts are needed and then dividing the number of records by the number of partitions. The last step is to select the records and assign them to each partition, and then save their info to a csv.

### Synthesize.py <part.csv> <outputDirectory>
Third step is to run the synthesize script. This feeds into the nuance nature of the previous algorithm, to avoid outliers affecting our final resolutions, we use the median resolution of each partition as the target, and crop/pad all the images within the partition to match the resolution and 1:1 aspect ratio. 

** The reasoning for this pipeline is to decrease the likelihood of images that are too cropped that the object isn't in frame, or over pad the image to where the image has too much whitespace.
