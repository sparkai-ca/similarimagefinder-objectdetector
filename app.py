import os
import cv2
from flask import Flask, render_template, request, jsonify
from searchengine.colordescriptor import DescriptorOfColors
from searchengine.searcher import ImageSearcher
from predict import predict
import matplotlib.pyplot as plt
# create flask instance
app = Flask(__name__)

INDEX = os.path.join(os.path.dirname(__file__), 'index.csv')


# Main route
@app.route('/')
def index():
    return render_template('index.html', preview="static/init-preview.png")


# image database url list route
@app.route('/list', methods=['POST'])
def get_image_list():

    if request.method == "POST":

        try:
            image_list = [img for img in list(os.listdir(os.path.join(os.path.dirname(__file__), 'static/images/')))
                          if img[-4:] in ('.png', '.jpg', '.gif')]

            return jsonify(imgList=image_list)

        except Exception as e:
            return jsonify({"sorry": "Sorry, no results! Please try again."}), 500


# search route
@app.route('/search', methods=['POST'])
def search():
 
    if request.method == "POST":
        results_array = []

        # Get image url
        image_url = request.form.get('img')
 
        try:
            # Initialize the image descriptor
            cd = DescriptorOfColors((8, 12, 3))
 
            # Load the query image and describe it
            query = cv2.imread(os.path.join(os.path.dirname(__file__), 'static/images/'+image_url))
            features = cd.describe(query)
 
            # Perform the search
            searcher = ImageSearcher(INDEX)
            results = searcher.search(features)
 
            # loop over the results, displaying the score and image name
            for score, resultID in results:
                results_array.append(
                    {"image": str(resultID), "score": str(score)})

            # return success
            return jsonify(results=(results_array[:10]), preview="images/"+image_url)
 
        except Exception as e:
            print(str(e))
            # return error
            return jsonify({"sorry": "Sorry, no results! Please try again."}), 500


@app.route('/object_detection', methods=['POST'])
def object_detection():
    if request.method == 'POST':
        try:
            # Get image url
            image_id = request.form.get('img')
            predicted_image = predict(os.path.join("images/", image_id))
            plt.imsave(os.path.join("Results", image_id), predicted_image)
            return jsonify(image=os.path.join("Results", image_id))
        except Exception as e:
            print(str(e))
            # return error
            return jsonify({"sorry": "Sorry, no results! Please try again."}), 500


# run!
if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)
