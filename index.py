from searchengine.colordescriptor import DescriptorOfColors
import argparse
import glob
import cv2
import os

# Construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dataset", required=True, help="path to the directory that contains the images to be indexed")
ap.add_argument("-i", "--index", required=True, help="path to where the index csv file should be stored")
args = vars(ap.parse_args())

# Initialize the color descriptor
cd = DescriptorOfColors((8, 12, 3))

if not os.path.isdir(args["index"]):
    print("--index should be a directory")
    exit()

# Open the output index file for writing
output = open(os.path.join(args["index"], "index.csv"), "w")
types = ('/*.jpg', '/*.png', '/*.gif')  # The tuple of file types
files_grabbed = []
for files in types:
    files_grabbed.extend(glob.glob(args["dataset"]+files))

# Loop over files
for imagePath in files_grabbed:
    # Extract the image name from the image
    imageID = imagePath[imagePath.rfind("/")+1:]
    # Load the image
    image = cv2.imread(imagePath)

    # Describe the image
    features = cd.describe(image)

    # Write the features to file
    features = [str(f) for f in features]
    output.write("%s,%s\n" % (imageID, ",".join(features)))

# close the index file
output.close()
