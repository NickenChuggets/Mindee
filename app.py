import sys
import io
import base64
import cv2
import numpy as np
from PIL import Image
from flask import Flask, request, render_template, jsonify
import images

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html', image=images.image, mask=images.mask)

@app.route('/images', methods=['POST'])
def upload():
	image_data = base64.b64decode(request.form['image'])
	mask_data = base64.b64decode(request.form['mask'])

	image_bytes = io.BytesIO(image_data)
	mask_bytes = io.BytesIO(mask_data)

	image = Image.open(image_bytes)
	mask = Image.open(mask_bytes)

	image_array = np.array(image)[:,:,0]
	mask_array = np.array(mask)[:,:]

	image_height = len(image_array)
	image_width = len(image_array[0])

	resized_mask = cv2.resize(mask_array, (image_width, image_height))

	first_line_found = False

	first_line = 0
	first_column = len(resized_mask[0])
	last_line = 0
	last_column = 0

	for i in range(len(resized_mask)):
		for j in range(len(resized_mask[0])):
			if resized_mask[i][j] == 1:
				if not first_line_found:
					first_line = i
					first_line_found = True
				if i > last_line:
					last_line = i
				if j < first_column:
					first_column = j
				elif j > last_column:
					last_column = j

	coordinates = ((first_line, first_column), (last_line, last_column))

	return render_template('base.html', coordinates=coordinates)