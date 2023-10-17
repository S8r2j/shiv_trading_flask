from db.model import db,app, products, granites,granitethick,granitephoto, thick
from flask import abort, Response, json, jsonify
from routes import upphoto
from flask_jwt_extended import jwt_required, current_user
from trends.trend import Trending

class Marbles:
    def __init__(self, product = None, thik = None, granite = None, file = None, trend = None):
        self.product = product
        self.thik   = thik
        self.granite = granite
        self.file = file
        self.trend = trend
    @jwt_required()
    def post_granites(self):
        user = current_user
        if not user:
            return jsonify({ "error": "User doesn't exist" }), 400
        if not user.issuperuser:
            return jsonify({ "error": "User not authorized to modify" }), 401
        product = self.product
        granite = self.granite
        thik = self.thik
        file = self.file
        query = products.query.filter(products.productname == product).first()
        if not query:
            abort(404, description = "No such product found")

        query = granites.query.filter(granites.category == granite).first()
        if not query:
            abort(404, description = "No such category of granites item found")

        tile_type = granitethick.query.join(products).join(granites).join(thick).filter(
            products.productname == product
        ).filter(products.productname == product).filter(granites.category == granite).filter(
            thick.thick == thik
        ).first()

        image_url = upphoto.upload_photo(file, "granitephotos")
        photo_address = image_url
        with app.app_context():
            try:
                upload_photo = granitephoto(photoaddress = photo_address, gtid = tile_type.gtid)
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

    def get_granites(self):
        granite = self.granite
        thik = self.thik
        if granite and granite != None:
            granite = granite.strip()
            is_size = granites.query.filter(granites.category == granite).first()
            if not is_size:
                abort(404)
        if thik and thik != None:
            thik = thik.strip()
            is_thick = thick.query.filter(thick.thick == thik).first()
            if not is_thick:
                abort(404)
        try:
            if granite != None and thik != None and granite and not granite.isspace() and thik and not thik.isspace():
                url = granitethick.query.join(granites).join(
                    thick
                    ).filter(
                    granites.category == granite
                ).filter(thick.thick == thik).all()
                details = []
                for row in url:
                    for photo in row.photoaddress:
                        ls = {
                            "size": thik,
                            "url": photo.photoaddress
                        }
                        details.append(ls)
                return Response(
                    json.dumps(details, ensure_ascii = False).encode('utf-8'),
                    content_type = 'application/json; charset=utf-8'
                )
            if not granite and thik != None and not thik.isspace():
                url = granitethick.query.join(thick).filter(thick.thick == thik).all()
                details = []
                for row in url:
                    for photo in row.photoaddress:
                        ls = {
                            "size": thik,
                            "url": photo.photoaddress
                        }
                        details.append(ls)
                return Response(
                    json.dumps(details, ensure_ascii = False).encode('utf-8'),
                    content_type = 'application/json; charset=utf-8'
                )
            if not thik and granite != None and not granite.isspace():
                url = granitephoto.query.join(granitethick).join(granites).filter(
                    granites.category == granite
                ).all()
                details = []
                for row in url:
                    size = thick.query.join(granitethick).join(granitephoto).filter(
                        granitephoto.gtid == row.gtid
                    ).first()
                    ls = {
                        "size": size.thick,
                        "url": row.photoaddress
                    }
                    details.append(ls)
                return Response(
                    json.dumps(details, ensure_ascii = False).encode('utf-8'),
                    content_type = 'application/json; charset=utf-8'
                )
            if not granite and not thik:
                url = granitephoto.query.join(granitethick).all()
                details = []
                for row in url:
                    size = thick.query.join(granitethick).join(granitephoto).filter(
                        granitephoto.gtid == row.gtid
                    ).first()
                    ls = {
                        "size": size.thick,
                        "url": row.photoaddress
                    }
                    details.append(ls)
                return Response(
                    json.dumps(details, ensure_ascii = False).encode('utf-8'),
                    content_type = 'application/json; charset=utf-8'
                )
        except Exception as e:
            return str(e)