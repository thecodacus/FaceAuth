############

import io
import cv2
import base64 
import numpy as np
from PIL import Image
import requests
import json
import pickle

from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler 


import os
from django.conf import settings
############


# convert PIL Image to an RGB image( technically a numpy array ) that's compatible with opencv
def toRGB(image):
    return cv2.cvtColor(np.array(image), cv2.COLOR_BGR2RGB)

# Take in base64 string and return PIL image
def stringToImage(base64_string):
    imgdata = base64.b64decode(base64_string)
    return toRGB(Image.open(io.BytesIO(imgdata)))

def resizeAndPad(img, size):
	h, w = img.shape[:2]

	sh, sw = size
	# interpolation method
	if h > sh or w > sw:  # shrinking image
		interp = cv2.INTER_AREA
	else: # stretching image
		interp = cv2.INTER_CUBIC

	# aspect ratio of image
	aspect = w/h

	# padding
	if aspect > 1: # horizontal image
		new_shape = list(img.shape)
		new_shape[0] = w
		new_shape[1] = w
		new_shape = tuple(new_shape)
		new_img=np.zeros(new_shape, dtype=np.uint8)
		h_offset=int((w-h)/2)
		new_img[h_offset:h_offset+h, :, :] = img.copy()

	elif aspect < 1: # vertical image
		new_shape = list(img.shape)
		new_shape[0] = h
		new_shape[1] = h
		new_shape = tuple(new_shape)
		new_img = np.zeros(new_shape,dtype=np.uint8)
		w_offset = int((h-w) / 2)
		new_img[:, w_offset:w_offset + w, :] = img.copy()
	else:
		new_img = img.copy()
	# scale and pad
	scaled_img = cv2.resize(new_img, size, interpolation=interp)
	return scaled_img



class Base64ToNpImage():
	def __init__(self):
		self.base64prefix="data:image/png;base64,"
	
	def decode(self, encoded):
		return stringToImage(encoded.split(',')[1])
	
	def decodeArray(self,encodedList):
		images=[]
		for value in encodedList:
			images.append(self.decode(value))

		return images

	def getDataURIFromEncoded(encoded):
		return self.base64prefix+encoded


class TensorflowBridge():
	
	def __init__(self):
		self.detector = cv2.CascadeClassifier(os.path.join(settings.BASE_DIR, 'assets/haarcascade_frontalface_default.xml'))
		self.API_ENDPOINT = "http://face-recog-model-server:8501/v1/models/model:predict"


	def imagesToFaces(self,images, size):
		finalFaces=[]
		for img in images:
			gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
			faces = self.detector.detectMultiScale(gray, 1.3, 5)
			area=0
			face=()
			for (x,y,w,h) in faces:
				if(w*h>area):
					area=w*h
					face=(x,y,w,h)
			if(area==0):
				continue
			(x,y,w,h)=face
			#saving the captured face in the dataset folder
			faceNp=np.array(img[y:y+h,x:x+w])
			faceNp=resizeAndPad(faceNp,size)
			finalFaces.append(faceNp);
		return finalFaces

	def prewhiten(self,xinp):
		x=xinp.astype(np.float)
		mean = np.mean(x)
		std = np.std(x)
		std_adj = np.maximum(std, 1.0/np.sqrt(x.size))
		y = np.multiply(np.subtract(x, mean), 1/std_adj)
		return y 

	def preprocessFaces(self,faces):
		ppFaces=[]
		for i in range(len(faces)):
			ppFaces.append(self.prewhiten(faces[i]))

		return ppFaces

	def embeddFaces(self,faces):
		faceNps=np.array(faces, dtype=np.float)
		listFaces=faceNps.tolist()
		print(len(listFaces[0]))
		postData = {
			#Optional: serving signature to use.
			#If unspecifed default serving signature is used.
			"signature_name": "encode",
			#List of tensors (each element must be of same shape and type)
			"instances": listFaces
		}
		r = requests.post(url = self.API_ENDPOINT, data = json.dumps(postData))

		return json.loads(r.content)['predictions']

class Recognizer():
	def __init__(self):
		self.classifier = KNeighborsClassifier(n_neighbors=3)

	def train(self,users):
		labels=[]
		signatureSamples=[]
		for user in users:
			if user.facesignature.signatures=="" or user.facesignature.signatures is None:
				continue

			signatures=pickle.loads(eval(user.facesignature.signatures))
			for signature in signatures:
				labels.append(user.id)
				signatureSamples.append(signature)

		self.classifier.fit(signatureSamples,labels)
		# open a file, where you ant to store the data
		file = open(os.path.join(settings.BASE_DIR, 'assets/knnModel.pkl'), 'wb')
		# dump information to that file
		pickle.dump(self.classifier, file)
		# close the file
		file.close()


	def predict(self,embeddFaces):
		# open a file, where you ant to store the data
		file = open(os.path.join(settings.BASE_DIR, 'assets/knnModel.pkl'), 'rb')
		# dump information to that file
		classifier=pickle.load(file)
		# close the file
		file.close()

		labels=classifier.predict(embeddFaces)
		print (labels)
		return labels



		











