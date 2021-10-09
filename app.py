#!flask/bin/python
from flask import Flask
from flask_cors import CORS
from flask import request, jsonify, abort
import bn_project
import json 

app = Flask(__name__)
CORS(app)

param_dict = {'': '', '': ''}

#default route, allows me to confirm the API is working
@app.route('/')
@app.route('/index')
def index():
	return "API is working!"

# A route to set evidence and return the updated outputs	
@app.route('/getall', methods=['POST'])
def postBnEvidence():
	if not request.json:
		abort(400)
	bn_params = json.dumps(request.json)
	output_dict = bn_project.updateBn(json.loads(bn_params))
	response = jsonify(output_dict)
	response.headers.add('Access-Control-Allow-Origin', '*')
	return response, 201	
	
	
# A route to return the baseline bn model without setting evidence.
@app.route('/getall', methods=['GET'])
def getBaseline():
	output_dict = bn_project.updateBn(param_dict)
	response = jsonify(output_dict)
	response.headers.add('Access-Control-Allow-Origin', '*')
	return response

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000, debug="on")

#EXAMPLE USING LINUX CURL
#curl -i -H "Content-Type: application/json" -X POST -d '{"Age": "Child", "Dysuria_1": "Recorded"}' http://bardai.io:5000/postbnevidence

#EXMAPLE USING WINDOWS
#curl.exe --% -i -X POST -H "Content-Type:application/json" -d "{  \"ci_age_group_bg\" : \"young\",  \"ci_metabolic_syndrome_bg\" : \"FALSE\" }" http://bardai.io:5000/postbnevidence

#deploy docker
#docker run -d --name cdap_api -p 5000:5000 cdap_ui:latest