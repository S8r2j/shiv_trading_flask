from db.model import db, app, basicfinish, standardfinish, premiumfinish
from flask import Response, json, jsonify
from flask_jwt_extended import jwt_required, current_user
from routes import upphoto


class Finishing:
    def __init__(self, plan, description = None):
        self.plan = plan
        self.description = description

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
                    ls = {
                        "url":row.photoaddress
                    }
                    if row.description:
                        ls["description"]= row.description
                    finish.append(ls)
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
                    ls = {
                        "url": row.photoaddress
                    }
                    if row.description:
                        ls["description"] = row.description
                    finish.append(ls)
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
                    ls = {
                        "url": row.photoaddress
                    }
                    if row.description:
                        ls["description"] = row.description
                    finish.append(ls)
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
            description = self.description
            if self.plan == "Basic":
                url = upphoto.upload_photo(file, "basic_finish")
                image_url = url["url"]
                file_id = url["file_id"]
                finish = basicfinish(photoaddress = image_url, imagekitid = file_id, description = description)
                db.session.add(finish)
                db.session.commit()
                db.session.refresh(finish)
                return "Uploaded photo of basic finish category"
            if self.plan == "Standard":
                url = upphoto.upload_photo(file, "standard_finish")
                image_url = url["url"]
                file_id = url["file_id"]
                finish = standardfinish(photoaddress = image_url, imagekitid = file_id, description = description)
                db.session.add(finish)
                db.session.commit()
                db.session.refresh(finish)
                return "Uploaded photo of standard finish category"
            if self.plan == "Premium":
                url = upphoto.upload_photo(file, "premium_finish")
                image_url = url["url"]
                file_id = url["file_id"]
                finish = premiumfinish(photoaddress = image_url, imagekitid = file_id, description = description)
                db.session.add(finish)
                db.session.commit()
                db.session.refresh(finish)
                return "Uploaded photo of premium finish category"