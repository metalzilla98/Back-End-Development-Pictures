from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    if(request.method == 'GET'): 
        return jsonify(data)

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):

    for picture in data:
        if picture["id"] == id:          
            return jsonify(picture)
    return jsonify({"message":"Resource not found"}), 404



######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    picture_post = request.get_json()   
    for picture in data:
        if picture["id"] == picture_post["id"]:
            message_content = f"picture with id {picture_post['id']} already present"
            return jsonify({"Message":message_content }), 302     
    data.append(picture_post)
    return jsonify(picture_post), 201

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    picture_for_update = request.get_json()
    for i in range(len(data)):
        if data[i]["id"] == id:
            data[i] = picture_for_update
            return jsonify(picture_for_update),200
    return jsonify({"message": "picture not found"}),404  

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    for i in range(len(data)):
        if data[i]["id"] == id:
            del data[i]    
            return "",204
    return jsonify({"message": "picture not found"}),404
