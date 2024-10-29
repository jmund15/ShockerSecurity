from flask import Blueprint, request, url_for, redirect, jsonify, render_template
from flask_login import LoginManager, login_required
#import jsonify

from flaskModels import Face
from flaskLogin import login_manager
from SQLiteConnect import getAllFaces, getAllFacesRaw, updateFace

faces = Blueprint('faces', __name__, template_folder='../frontend')
#login_manager = LoginManager()
#login_manager.init_app(faces)

#current_faces = list[Face]

@faces.route('/faces', methods=['GET'])
@login_required
def show():
    return render_template('faces.html',title='Security Management')


@faces.route('/faces/data', methods=['GET'])
#@login_required
def get_faces():
    faces = getAllFaces()
    #print('raw faces: \n', faces)
    faceJson = jsonify([face.to_dict() for face in faces])
    print(faceJson)
    return faceJson

@faces.route('/faces/update', methods=['POST'])
@login_required
def update_face():
    data = request.json
    id = data['id']
    name = data['name']
    accepted = data['accepted']
    if (updateFace(id, name, accepted)):
        return jsonify({'message': 'Updated successfully'})
    else:
        return jsonify({'message': 'Error updated face!'})