from db.model import db,app, products, sizes, rooms, tilesphotos, productroomsize, trendingproduct
from flask import abort, Response, json, jsonify
from routes import upphoto
from flask_jwt_extended import jwt_required, current_user
from trends.trend import Trending

class Tiles:
    def __init__(self, product = None, size = None, room = None, file = None, trend = None, description = None):
        self.product = product
        self.size = size
        self.room = room
        self.file = file
        self.trend = trend
        self.description = description
    def get_tiles(self):
        product = self.product
        size = self.size
        room = self.room
        with app.app_context():
            if product and product != None:
                product = product.strip()
                is_product = products.query.filter_by(productname = product).first()
                if not is_product:
                    abort(404)
            if size and size != None:
                size = size.strip()
                is_size = sizes.query.filter_by(sizes = size).first()
                if not is_size:
                    abort(404)
            if room and room != None:
                room = room.strip()
                with app.app_context():
                    query = db.session.query(rooms).filter(rooms.roomname == room)
                    is_room = query.first()
                    if not is_room:
                        abort(404)
            try:
                if product != None and room != None and size != None and product and not product.isspace() and room and not room.isspace() and size and not size.isspace():
                    url = productroomsize.query.join(rooms).join(products).join(sizes).filter(sizes.sizes == size, products.productname == product, rooms.roomname == room).first()
                    details = []
                    for row in url.tilesphotos:
                        ls = {
                            "size": size,
                            "url": row.photoaddress
                        }
                        if row.description:
                            ls["description"] = row.description
                        details.append(ls)
                    return Response(json.dumps(details, ensure_ascii=False).encode('utf-8'), content_type='application/json; charset=utf-8')
                if not size and product != None and not product.isspace() and room != None and not room.isspace():
                    url = productroomsize.query.join(rooms).join(products).\
                        filter(
                        products.productname == product, rooms.roomname == room
                    ).all()
                    details = []
                    for row in url:
                        size = sizes.query.join(productroomsize).join(tilesphotos).filter(
                            tilesphotos.prsid == row.prsid
                        ).first()
                        for photo in row.tilesphotos:
                            ls = {
                                "size": size.sizes,
                                "url": photo.photoaddress
                            }
                            if photo.description:
                                ls["description"] = row.description
                            details.append(ls)
                    return Response(json.dumps(details, ensure_ascii=False).encode('utf-8'), content_type='application/json; charset=utf-8')
                if not room and product != None and not product.isspace() and size != None and not size.isspace():
                    url = productroomsize.query.join(sizes).join(
                        products
                        ).filter(
                        products.productname == product, sizes.sizes == size
                    ).all()
                    details = []
                    for row in url:
                        for photo in row.tilesphotos:
                            ls = {
                                "size": size,
                                "url": photo.photoaddress
                            }
                            if photo.description:
                                ls["description"] = row.description
                            details.append(ls)
                    return Response(json.dumps(details, ensure_ascii=False).encode('utf-8'), content_type='application/json; charset=utf-8')
                if not room and not size and product != None and not product.isspace():
                    url = productroomsize.query.join(products).filter(
                        products.productname == product
                    ).all()
                    details = []
                    for row in url:
                        size = sizes.query.join(productroomsize).join(tilesphotos).filter(
                            tilesphotos.prsid == row.prsid
                        ).first()
                        for photo in row.tilesphotos:
                            ls = {
                                "size": size.sizes,
                                "url": photo.photoaddress
                            }
                            if photo.description:
                                ls["description"] = row.description
                            details.append(ls)
                    return Response(json.dumps(details, ensure_ascii=False).encode('utf-8'), content_type='application/json; charset=utf-8')
                if not product and size != None and not size.isspace() and room != None and not room.isspace():
                    url = productroomsize.query.join(rooms).join(sizes).filter(
                            rooms.roomname == room, sizes.sizes == size
                    ).all()
                    details = []
                    for row in url:
                        for photo in row.tilesphotos:
                            ls = {
                                "size": size,
                                "url": photo.photoaddress
                            }
                            print(photo.description)
                            if photo.description:
                                ls["description"] = row.description
                            details.append(ls)
                    return Response(json.dumps(details, ensure_ascii=False).encode('utf-8'), content_type='application/json; charset=utf-8')
                if not product and not size and room != None and not room.isspace():
                    url = productroomsize.query.join(rooms).filter(
                        rooms.roomname == room
                    ).all()
                    details = []
                    for row in url:
                        size = sizes.query.join(productroomsize).join(tilesphotos).filter(
                            tilesphotos.prsid == row.prsid
                        ).first()
                        for photo in row.tilesphotos:
                            ls = {
                                "size": size.sizes,
                                "url": photo.photoaddress
                            }
                            if photo.description:
                                ls["description"] = row.description
                            details.append(ls)
                    return Response(json.dumps(details, ensure_ascii=False).encode('utf-8'), content_type='application/json; charset=utf-8')
                if not product and not room and size != None and not size.isspace():
                    url = productroomsize.query.join(sizes).filter(
                        sizes.sizes == size
                    ).all()
                    details = []
                    for row in url:
                        for photo in row.tilesphotos:
                            ls = {
                                "size": size,
                                "url": photo.photoaddress
                            }
                            if photo.description:
                                ls["description"] = row.description
                            details.append(ls)
                    return Response(json.dumps(details, ensure_ascii=False).encode('utf-8'), content_type='application/json; charset=utf-8')
                if not product and not room and not size:
                    url = productroomsize.query.all()
                    details = []
                    for row in url:
                        size = sizes.query.join(productroomsize).join(tilesphotos).filter(
                            tilesphotos.prsid == row.prsid
                        ).first()
                        for photo in row.tilesphotos:
                            ls = {
                                "size": size.sizes,
                                "url": photo.photoaddress
                            }
                            if photo.description:
                                ls["description"] = row.description
                            details.append(ls)
                    return Response(
                            json.dumps(details, ensure_ascii = False).encode('utf-8'),
                            content_type = 'application/json; charset=utf-8'
                            )
            except Exception as e:
                return str(e)

    @jwt_required()
    def post_tiles(self):
        user = current_user
        if not user:
            return jsonify({ "error": "User doesn't exist" }), 400
        if not user.issuperuser:
            return jsonify({ "error": "User not authorized to modify" }), 401
        product = self.product
        size = self.size
        room = self.room
        trend = self.trend
        description = self.description
        query = products.query.filter(products.productname == product).first()
        if not query:
            abort(404)

        query = sizes.query.filter(sizes.sizes == size).first()
        if not query:
            abort(404)

        query = rooms.query.filter(rooms.roomname == room).first()
        if not query:
            abort(404)

        tile_type = productroomsize.query.join(products).join(sizes).join(rooms).filter(
            products.productname == product,
            rooms.roomname == room,
            sizes.sizes == size
        ).first()

        file = self.file

        url = upphoto.upload_photo(file, "tiles")
        image_url = url["url"]
        file_id = url["file_id"]
        photo_address = image_url
        with app.app_context():
            try:
                upload_photo = tilesphotos(photoaddress = photo_address, prsid = tile_type.prsid, imagekitid = file_id, description = description)
                db.session.add(upload_photo)
                db.session.commit()
                if trend == "True":
                    product = Trending()
                    response = product.post_trending_products(photourl = photo_address)
                    return response
                return "Photo uploaded successfully"
            except Exception as e:
                return jsonify({"error":f"{str(e)}"}), 500