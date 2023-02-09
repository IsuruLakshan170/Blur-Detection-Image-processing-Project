from app import app
from flask import Flask, flash, request, redirect, render_template
from werkzeug.utils import secure_filename
import cv2
import numpy as np
import io
from PIL import Image
import base64
from Helpers import *
from enhancement import *

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
	
@app.route('/')
def upload_form():
	return render_template('upload.html')


@app.route('/', methods=['POST'])
def upload_image():
	images = []
	for file in request.files.getlist("file[]"):
		print("***************************")
		print("image: ", file)
		if file.filename == '':
			flash('No image selected for uploading')
			return redirect(request.url)
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			filestr = file.read()
			npimg = np.frombuffer(filestr, np.uint8)
			image = cv2.imdecode(npimg, cv2.IMREAD_UNCHANGED)
			ratio = image.shape[0] / 500.0
			orig = image.copy()
			image = Helpers.resize(image, height = 500)

			gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
			fm = cv2.Laplacian(gray, cv2.CV_64F).var()
			result = "Not Blurry"

			if fm < 100:
				result = "Blurry"

			sharpness_value = "{:.0f}".format(fm)

			recoveredImage = enhancement.recoverImage(image)
			cv2.imwrite("processed_image.png",recoveredImage)

			message = [result,sharpness_value,recoveredImage]
			# print(recoveredImage)
			img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
			# print(image)
			file_object = io.BytesIO()
			img= Image.fromarray(Helpers.resize(img,width=500))
			img.save(file_object, 'PNG')
			base64img = "data:image/png;base64,"+base64.b64encode(file_object.getvalue()).decode('ascii')
   			
			file_object2 = io.BytesIO()
			img2= Image.fromarray(recoveredImage)
			img2.save(file_object2, 'PNG')
			base64img2 = "data:image/png;base64,"+base64.b64encode(file_object2.getvalue()).decode('ascii')
   			
      
			images.append([message,base64img,base64img2])
			
			
	print("images:", len(images))
	print(images[0][0][1])
	print(images[0][0][2])
	# print(images[0][1])
 
	return render_template('upload.html', images=images )
	

if __name__ == "__main__":
    app.run(debug=True)