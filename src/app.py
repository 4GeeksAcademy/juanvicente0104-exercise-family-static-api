"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os, json
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def handle_hello():
    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    #response_body = {
    #    "hello": "world",
    #    "family": members
    #}
    return jsonify(members)

@app.route('/member',methods=['POST'])
def add_member():
    body = request.json
    member = jackson_family.add_member(body)

    if member == True:
        return jsonify(member), 200
    else:
        return jsonify({"message":"Fill all the fields"}), 400

@app.route('/member/<int:id>',methods=['DELETE'])
def delete_member(id):
    member = jackson_family.delete_member(id)

    if member == "last":
        return jsonify({"message":"You can not delete the last family member"}), 401
    elif member == True:
        return jsonify({'done':member}), 200
    else:
        return jsonify({"message":"Family member not found"}), 404
    
@app.route('/member/<int:id>',methods=['GET'])
def get_member(id):
    member = jackson_family.get_member(id)

    if member is not False:
        return jsonify(member), 200
        ##return jsonify([member.first_name,member.id,member.age,member.lucky_numbers]), 200
    else:
        return jsonify({"message":"Family member not found"}), 404

@app.route('/member/<int:id>',methods=['PUT'])
def update_member(id):
    body = json.loads(request.data)
    member = jackson_family.update_member(id,body)

    if member is not False:
        return jsonify(member), 200
    else:
        return jsonify({"message":"Member not found"}), 404

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
