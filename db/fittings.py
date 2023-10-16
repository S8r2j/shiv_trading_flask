from db.model import db,app, products, cpfittings, cpphotos, productfitting
from flask import abort, Response, json, jsonify
from routes import upphoto
from flask_jwt_extended import jwt_required, current_user

class Sanitary:
    def __init__(self, product = None, fitting_name = None, file = None):
        self.product = product
        self.fitting_name =fitting_name
        self.file = file

    def get_fittings(self):
        fittingname = self.fitting_name
        details = []
        with app.app_context():
            if not fittingname:
                photo = cpphotos.query.all()
                for row in photo:
                    details.append(row.photoaddress)
            if fittingname:
                query = cpfittings.query.filter(cpfittings.fittingname == fittingname).first()
                if not query:
                    abort(404)
                photo = productfitting.query.join(cpfittings).filter(cpfittings.fittingname == fittingname).all()
                for row in photo:
                    for photos in row.photoaddress:
                        details.append(photos.photoaddress)

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
        image_url = upphoto.upload_photo(up_photo, "cpphotos")
        photo_address = image_url
        with app.app_context():
            upload_photo = cpphotos(photoaddress = photo_address, pfittingid = tile_type.pfittingid)
            db.session.add(upload_photo)
            db.session.commit()
            db.session.refresh(upload_photo)

        return { "message": "Photo uploaded successfully" }