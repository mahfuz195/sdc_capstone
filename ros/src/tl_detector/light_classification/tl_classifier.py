from styx_msgs.msg import TrafficLight
import cv2
from keras.models import load_model
from numpy import zeros, newaxis
import rospkg
import numpy as np
import tensorflow as tf
import os
from keras.utils.generic_utils import CustomObjectScope
import keras
from keras.preprocessing import image


class TLClassifier(object):
    def __init__(self):
        #TODO load classifier
	curr_dir = os.path.dirname(os.path.realpath(__file__))
        self.model = load_model(curr_dir+ '/model_2.h5') 
        # get prepared for the future.
        #with CustomObjectScope({'relu6': keras.applications.mobilenet.relu6,'DepthwiseConv2D': keras.applications.mobilenet.DepthwiseConv2D}):
        #model = load_model('weights.hdf5')
        #    self.model = load_model(curr_dir + '/test_1.h5') 
        
        self.model._make_predict_function()
        self.graph = tf.get_default_graph()
        self.TL_RED = 1
        self.STATUS = ['GREEN','RED']
        #pass
    def process_image(self,img):
        img_tensor = image.img_to_array(img)                    # (height, width, channels)
        img_tensor = np.expand_dims(img_tensor, axis=0)         # (1, height, width, channels), add a dimension because the model expects this shape: (batch_size, height, width, channels)
        img_tensor /= 255. 

        return img_tensor   

    def get_classification(self, image):
        """Determines the color of the traffic light in the image

        Args:
            image (cv::Mat): image containing the traffic light

        Returns:
            int: ID of traffic light color (specified in styx_msgs/TrafficLight)

        """
        #TODO implement light color prediction
        imrs = cv2.resize(image, (400, 400)) 

        #img_tensor = self.process_image(img)
        #pred = self.model.predict(img_tensor)
        #predicted_class = np.argmax(pred, axis=1)
        #print('Predicted Class:' ,predicted_class[0] , ' : ', self.STATUS[predicted_class[0]])
        #light_status = predicted_class[0]
        imrs = imrs.astype(float)
        imrs = imrs / 255.0
        imrs = imrs[newaxis,:,:,:]
        #print(imrs)
        with self.graph.as_default():
            preds = self.model.predict(imrs)
            print('Predicted:' ,preds)
            predicted_class = np.argmax(preds, axis=1)
            print('Predicted Class:' ,predicted_class[0] , ' : ', self.STATUS[predicted_class[0]])
            light_status = predicted_class[0]

            if(light_status == self.TL_RED):
                return TrafficLight.RED
        # otherwise return unknown
        return TrafficLight.UNKNOWN
