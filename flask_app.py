import json
import os
from flask import Flask,jsonify,request
from flask_cors import CORS
from model import prediction
import tensorflow as tf
import base64
import ast



app = Flask(__name__)
CORS(app)

predictionObj = prediction()

@app.route("/predict/",methods=['POST','GET'])
def predict():
	try:
		encoded_string = request.form.get('BASE64')
		# image = 'pi2235-03-3.jpg'
		# encoded_string = ""
		# with open(image, "rb") as image_file:
		#     encoded_string = base64.b64encode(image_file.read())

		ret, predicted_class, name, family, author = predictionObj.predict(encoded_string)

		if not ret:
			ret_dict = {
			'Error':True,
			'Message':'Error in prediction'
						}
			return jsonify(ret_dict)

		ret_dict = {
					'Error': False,
					'Scientific_name':predicted_class,
					'Actual_name':name,
					'Family':family,
					'Author':author
					}
		return jsonify(ret_dict)
	except Exception as e:
		print ("Exception ", e)
		ret_dict = {
		'Error':True,
		'Message':e
					}
		return jsonify(ret_dict)


@app.route("/search/",methods=['POST','GET'])
def search():
	try:
		query = request.form.get('Query')
		# query = 'abies concolor'
		query = ast.literal_eval(query)
		name, family, author = predictionObj.get_details(query)

		ret_dict = {
					'Error': False,
					'Actual_name':name,
					'Family':family,
					'Author':author
					}
		return jsonify(ret_dict)
	except Exception as e:
		print ("Exception ", e)
		ret_dict = {
		'Error':True,
		'Message':e
					}
		return jsonify(ret_dict)

if __name__ == "__main__":
	app.run() 
