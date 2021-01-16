import os
import sys
import numpy as np
from mrcnn import visualize
from PIL import Image
import tensorflow as tf


os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'

# Root directory of the project
ROOT_DIR = os.path.abspath("./")
# Import Mask RCNN
sys.path.append(ROOT_DIR)  # To find local version of the library
from mrcnn.config import Config
from mrcnn import model as modellib, utils


############################################################
#  Configurations
############################################################

class GenericConfig(Config):
    """Configuration for training on the toy  dataset.
    Derives from the base Config class and overrides some values.
    """

    def __init__(self, classes, steps):
        self.NUM_CLASSES = classes
        self.STEPS_PER_EPOCH = steps
        self.BACKBONE = "mobilenetv1"
        super().__init__()

    # Give the configuration a recognizable name
    NAME = "class"

    # We use a GPU with 12GB memory, which can fit two images.
    # Adjust down if you use a smaller GPU.
    IMAGES_PER_GPU = 1
    GPU_COUNT = 1

    # Skip detections with < 90% confidence
    DETECTION_MIN_CONFIDENCE = 0.751
    IMAGE_MAX_DIM = 448
    IMAGE_MIN_DIM = 384
    # TRAIN_ROIS_PER_IMAGE = 20
    DETECTION_NMS_THRESHOLD = 0.2
    # DETECTION_MAX_INSTANCES = 3


labels = ["person","bicycle","car","motorcycle","airplane","bus","train","truck","boat","trafficlight","firehydrant","stopsign","parkingmeter","bench","bird","cat","dog","horse","sheep","cow","elephant","bear","zebra","giraffe","backpack","umbrella","handbag","tie","suitcase","frisbee","skis","snowboard","sportsball","kite","baseballbat","baseballglove","skateboard","surfboard","tennisracket","bottle","wineglass","cup","fork","knife","spoon","bowl","banana","apple","sandwich","orange","broccoli","carrot","hotdog","pizza","donut","cake","chair","couch","pottedplant","bed","diningtable","toilet","tv","laptop","mouse","remote","keyboard","cellphone","microwave","oven","toaster","sink","refrigerator","book","clock","vase","scissors","teddybear","hairdrier","toothbrush"]
weights_path = "static/mobile_mask_rcnn_coco.h5"
MODEL_DIR = "/".join(weights_path.split("/")[:-2])
config = GenericConfig(81, 1)

# Create model in inference mode
with tf.device("/cpu:0"):
    model = modellib.MaskRCNN(mode="inference", model_dir=MODEL_DIR, config=config)
model.load_weights(weights_path, by_name=True)
model.keras_model._make_predict_function()
print("Weights loaded")


def predict(image_path):

    image = Image.open(image_path).convert('RGB')
    image = np.array(image)
    results = model.detect([image], verbose=2)

    r = results[0]

    classes = ["background"]
    classes += labels
    image = visualize.draw_bbox(image, r['rois'], r['class_ids'], r['scores'], classes)

    return image

