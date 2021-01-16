# import the necessary packages
import numpy as np
import csv


def chi_squared_distance(histogramA, histogramB, eps=1e-10):
	# Compute chi squared distance
	distance = 0.5 * np.sum([((a-b)**2)/(a+b+eps) for (a, b) in zip(histogramA, histogramB)])

	# Return the chi squared distance
	return distance


class ImageSearcher:
	def __init__(self, csv_path):
		self.csv_path = csv_path

	def search(self, query_features, limit=10):
		# Initialize dictionary of results
		results = {}

		# Open the file
		with open(self.csv_path) as f:
			# Initialize the CSV reader
			csv_file = csv.reader(f)

			# Loop over the rows of csv file
			for row in csv_file:
				# Parse out the image ID and features
				features = [float(x) for x in row[1:]]

				# Calculate the chi squared distance between the features in our csv file row and our query features
				d = chi_squared_distance(features, query_features)

				# Dictionary key is image id, value is similarity
				results[row[0]] = d

			# Close csv reader
			f.close()

		# Sort the dictionary
		results = sorted([(v, k) for (k, v) in results.items()])

		# Return our limited results
		return results[:limit]
