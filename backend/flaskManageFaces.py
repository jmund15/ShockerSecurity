from flask import Blueprint, request, url_for, redirect
from flask_login import LoginManager, login_required
import jsonify

from flaskModels import Face
from flaskLogin import login_manager
from SQLiteConnect import getAllFaces, getAllFacesRaw, updateFace

faces = Blueprint('faces', __name__, template_folder='../frontend')
#login_manager = LoginManager()
#login_manager.init_app(faces)

#current_faces = list[Face]

@faces.route('/faces', methods=['GET'])
@login_required
def get_faces():
    faces = getAllFaces()
    print('raw faces: \n', faces)
    return jsonify([dict(face) for face in faces])

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