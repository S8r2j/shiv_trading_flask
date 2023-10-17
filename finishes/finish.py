from db.model import db, app, basicfinish, standardfinish, premiumfinish
from flask import Response, json, jsonify
from flask_jwt_extended import jwt_required, current_user
from routes import upphoto


class Finishing:
    def __init__(self, plan):
        self.plan = plan

    @jwt_required()
    def get_finish_photos(self):
        user = current_user
        if not user:
            return jsonify({ "error": "User doesn't exist" }), 400
        if not user.issuperuser:
            return jsonify({ "error": "User not authorized to modify" }), 401
        if self.plan == "Basic":
            query = basicfinish.query.all()
            finish = []
            if query:
                for row in query:
                    finish.append(row.photoaddress)
                return Response(
                    json.dumps(finish, ensure_ascii = False).encode('utf-8'),
                    content_type = 'application/json; charset=utf-8'
                )
            else:
                return jsonify({"error":"Photos for basic finishes not found"}), 400
        if self.plan == "Standard":
            query = standardfinish.query.all()
            finish = []
            if query:
                for row in query:
                    finish.append(row.photoaddress)
                return Response(
                    json.dumps(finish, ensure_ascii = False).encode('utf-8'),
                    content_type = 'application/json; charset=utf-8'
                )
            else:
                return jsonify({ "error": "Photos for standard finishes not found" }), 400
        if self.plan == "Premium":
            query = premiumfinish.query.all()
            finish = []
            if query:
                for row in query:
                    finish.append(row.photoaddress)
                return Response(
                    json.dumps(finish, ensure_ascii = False).encode('utf-8'),
                    content_type = 'application/json; charset=utf-8'
                )
            else:
                return jsonify({"error":"Photos for premium finishes not found"}), 400

    @jwt_required()
    def post_finish_photos(self, file):
        user = current_user
        if not user:
            return jsonify({ "error": "User doesn't exist" }), 400
        if not user.issuperuser:
            return jsonify({ "error": "User not authorized to modify" }), 401
        with app.app_context():
            if self.plan == "Basic":
                image_url = upphoto.upload_photo(file, "basic_finish")
                finish = basicfinish(photoaddress = image_url)
                db.session.add(finish)
                db.session.commit()
                db.session.refresh(finish)
                return "Uploaded photo of basic finish category"
            if self.plan == "Standard":
                image_url = upphoto.upload_photo(file, "standard_finish")
                finish = standardfinish(photoaddress = image_url)
                db.session.add(finish)
                db.session.commit()
                db.session.refresh(finish)
                return "Uploaded photo of standard finish category"
            if self.plan == "Premium":
                image_url = upphoto.upload_photo(file, "premium_finish")
                finish = premiumfinish(photoaddress = image_url)
                db.session.add(finish)
                db.session.commit()
                db.session.refresh(finish)
                return "Uploaded photo of premium finish category"