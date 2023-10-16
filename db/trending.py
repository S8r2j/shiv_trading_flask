from flask import abort, Response, json, jsonify
from routes import upphoto
from flask_jwt_extended import jwt_required, current_user