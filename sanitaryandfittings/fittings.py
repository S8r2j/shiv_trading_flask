from db.model import db,app, products, cpfittings, cpphotos, productfitting
from flask import abort, Response, json, jsonify
from routes import upphoto
from flask_jwt_extended import jwt_required, current_user
from trends.trend import Trending

class Sanitary:
    def __init__(self, product = None, fitting_name = None, file = None, trend = None, description = None):
        self.product = product
        self.fitting_name =fitting_name
        self.file = file
        self.trend = trend
        self.description = description

    def get_fittings(self):
        fittingname = self.fitting_name
        details = []
        with app.app_context():
            if not fittingname:
                photo = cpphotos.query.all()
                for row in photo:
                    ls = {
                        "url": row.photoaddress
                    }
                    if row.description:
                        ls["description"] = row.description
                    details.append(ls)
            if fittingname:
                query = cpfittings.query.filter(cpfittings.fittingname == fittingname).first()
                if not query:
                    abort(404)
                photo = productfitting.query.join(cpfittings).filter(cpfittings.fittingname == fittingname).all()
                for row in photo:
                    for photos in row.photoaddress:
                        ls = {
                            "url":photos.photoaddress
                        }
                        if photos.description:
                            ls["description"] = photos.description
                        details.append(ls)

            return Response(
                json.dumps(details, ensure_ascii = False).encode('utf-8'),
                content_type = 'application/json; charset=utf-8'
            )

    @jwt_required()
    def post_fittings(self):
        user = current_user
        if not user:
            return jsonify({ "error": "User doesn't exist" }), 400
        if not user.issuperuser:
            return jsonify({ "error": "User not authorized to modify" }), 401
        product = self.product
        fitting_name = self.fitting_name
        file = self.file
        description = self.description
        query = products.query.filter(products.productname == product).first()
        if not query:
            abort(404, description = "No such product found")

        query = cpfittings.query.filter(cpfittings.fittingname == fitting_name).first()
        if not query:
            abort(404, description = "No such CP Fitting and Sanitary item found")

        tile_type = productfitting.query.join(products).join(cpfittings).filter(
            products.productname == product,
            cpfittings.fittingname == fitting_name
        ).first()
        up_photo = file
        url = upphoto.upload_photo(up_photo, "cpphotos")
        image_url = url["url"]
        file_id = url["file_id"]
        photo_address = image_url
        with app.app_context():
            try:
                upload_photo = cpphotos(photoaddress = photo_address, pfittingid = tile_type.pfittingid, imagekitid = file_id, description = description)
                db.session.add(upload_photo)
                db.session.commit()
                db.session.refresh(upload_photo)
                if self.trend == "True":
                    product = Trending()
                    response = product.post_trending_products(photourl = photo_address)
                    return response
                return "Photo uploaded successfully"
            except Exception as e:
                return jsonify({"error":f"{str(e)}"}), 500


    @jwt_required()
    def remove_cpfitting_photos(self, url):
        user = current_user
        if not user:
            return jsonify({ "error": "User doesn't exist" }), 400
        if not user.issuperuser:
            return jsonify({ "error": "User not authorized to modify" }), 401
        query = cpphotos.query.filter(cpphotos.photoaddress == url).first()
        if not query:
            return jsonify({ "error": "No such url found" }), 400
        response = upphoto.delete_photos(query.imagekitid)
        db.session.delete(query)
        db.session.commit()
        return response