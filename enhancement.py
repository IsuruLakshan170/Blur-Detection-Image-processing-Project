import cv2
import numpy as np

class enhancement:
	def __init__(self):
		pass

	def recoverImage(image):
		newImage = cv2.cvtColor(cv2.fastNlMeansDenoisingColored(image, None, 0, 0, 0, 21), cv2.COLOR_BGR2RGB)    
        
		return newImage
