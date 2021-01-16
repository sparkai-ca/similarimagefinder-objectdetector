# import the necessary packages
import numpy as np
import cv2


class DescriptorOfColors:
	def __init__(self, bins):
		# store the number of bins for the 3D histogram
		self.num_bins = bins

	def describe(self, image):
		# convert the image to the HSV color space
		input_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
		# the features used to quantify the image
		features_list = []

		(height, width) = input_image.shape[:2]
		# Compute the center of the image
		# Divide the image height and width by 50%
		(coordinateX, coordinateY) = (int(width * 0.5), int(height * 0.5))

		# Segments of image (top-left, top-right, bottom-right, bottom-left)
		image_segments = [(0, coordinateX, 0, coordinateY),
						(coordinateX, width, 0, coordinateY),
						(coordinateX, width, coordinateY, height),
						(0, coordinateX, coordinateY, height)]

		# Elliptical mask representing the center of the image
		(axesX, axesY) = (int(width * 0.75) // 2, int(height * 0.75) // 2)
		mask_ellipse = np.zeros(input_image.shape[:2], dtype="uint8")
		cv2.ellipse(mask_ellipse, (coordinateX, coordinateY), (axesX, axesY), 0, 0, 360, 255, -1)

		# loop over the segments
		for (startX, endX, startY, endY) in image_segments:
			# construct a mask for each corner of the image, subtracting
			# the elliptical center from it
			corner_mask = np.zeros(input_image.shape[:2], dtype="uint8")
			cv2.rectangle(corner_mask, (startX, startY), (endX, endY), 255, -1)
			corner_mask = cv2.subtract(corner_mask, mask_ellipse)

			# Create a color histogram from the image
			histogram = self.create_histogram(input_image, corner_mask)
			# Update the feature vector
			features_list.extend(histogram)

		# Create a color histogram from the elliptical region
		histogram = self.create_histogram(input_image, mask_ellipse)
		# Update the feature vector
		features_list.extend(histogram)

		# return the feature vector
		return features_list

	def create_histogram(self, image, mask):
		# Create a 3D color histogram from the masked region of the image, using the given number of bins per channel
		histogram = cv2.calcHist([image], [0, 1, 2], mask, self.num_bins, [0, 180, 0, 256, 0, 256])
		# Normalize the histogram
		cv2.normalize(histogram, histogram)
		# Flatten the histogram
		histogram = histogram.flatten()

		# Return the histogram
		return histogram
