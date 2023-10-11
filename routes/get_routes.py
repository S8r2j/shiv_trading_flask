from flask import request, abort
from db.model import db,app, products, sizes, rooms, tiles_photos, product_room_size

@app.route("/tiles/photos", methods = ['GET'])
def get_tiles_photos():
    product = request.args.get('product', default = None, type = str)
    size = request.args.get('size', default = None, type = str)
    room = request.args.get('room', default = None, type = str)
    with app.app_context():
        if product and product != None:
            product = product.strip()
            is_product = products.query.filter_by(product_name = product).first()
            if not is_product:
                abort(404)
        if size and size != None:
            size = size.strip()
            is_size = sizes.query.filter_by(sizes = size).first()
            if not is_size:
                abort(404)
        if room and room != None:
            room = room.strip()
            is_room = rooms.query.filter(room_name = room).first()
            if not is_room:
                abort(404)
        try:
            if product != None and room != None and size != None and product and not product.isspace() and room and not room.isspace() and size and not size.isspace():
                query = db.session.query(product_room_size).join(rooms).join(sizes).join(products).filter(sizes.sizes == size).filter(products.product_name == product).filter(rooms.room_name == room)
                url = query.all()
                details = []
                for row in url:
                    query = db.session.query(sizes).join(product_room_size).join(tiles_photos).filter(tiles_photos.prs_id  == row.prs_id)
                    size = query.all()
                    ls = {
                        "size": size.sizes,
                        "url": row.photo_address
                    }
                    details.append(ls)
                return details
            if not size and product != None and not product.isspace() and room != None and not room.isspace():
                url = db.query(model.tiles_photos).join(model.product_room_size).join(model.rooms).join(
                    model.product
                ).filter(
                    model.product.product_name == product, model.rooms.room_name == room
                ).all()
                details = []
                for row in url:
                    size = db.query(model.size).join(model.product_room_size).join(model.tiles_photos).filter(
                        model.tiles_photos.prs_id == row.prs_id
                    ).first()
                    ls = {
                        "size": size.sizes,
                        "url": row.photo_address
                    }
                    details.append(ls)
                return details
            if not room and product != None and not product.isspace() and size != None and not size.isspace():
                url = db.query(model.tiles_photos).join(model.product_room_size).join(model.size).join(
                    model.product
                    ).filter(
                    model.product.product_name == product, model.size.sizes == size
                ).all()
                details = []
                for row in url:
                    size = db.query(model.size).join(model.product_room_size).join(model.tiles_photos).filter(
                        model.tiles_photos.prs_id == row.prs_id
                    ).first()
                    ls = {
                        "size": size.sizes,
                        "url": row.photo_address
                    }
                    details.append(ls)
                return details
            if not room and not size and product != None and not product.isspace():
                url = db.query(model.tiles_photos).join(model.product_room_size).join(model.product).filter(
                    model.product.product_name == product
                ).all()
                details = []
                for row in url:
                    size = db.query(model.size).join(model.product_room_size).join(model.tiles_photos).filter(
                        model.tiles_photos.prs_id == row.prs_id
                    ).first()
                    ls = {
                        "size": size.sizes,
                        "url": row.photo_address
                    }
                    details.append(ls)
                return details
            if not product and size != None and not size.isspace() and room != None and not room.isspace():
                url = db.query(model.tiles_photos).join(model.product_room_size).join(model.rooms).join(model.size).filter(
                    model.rooms.room_name == room, model.size.sizes == size
                ).all()
                details = []
                for row in url:
                    size = db.query(model.size).join(model.product_room_size).join(model.tiles_photos).filter(
                        model.tiles_photos.prs_id == row.prs_id
                    ).first()
                    ls = {
                        "size": size.sizes,
                        "url": row.photo_address
                    }
                    details.append(ls)
                return details
            if not product and not size and room != None and not room.isspace():
                url = db.query(model.tiles_photos).join(model.product_room_size).join(model.rooms).filter(
                    model.rooms.room_name == room
                ).all()
                details = []
                for row in url:
                    size = db.query(model.size).join(model.product_room_size).join(model.tiles_photos).filter(
                        model.tiles_photos.prs_id == row.prs_id
                    ).first()
                    ls = {
                        "size": size.sizes,
                        "url": row.photo_address
                    }
                    details.append(ls)
                return details
            if not product and not room and size != None and not size.isspace():
                url = db.query(model.tiles_photos).join(model.product_room_size).join(model.size).filter(
                    model.size.sizes == size
                ).all()
                details = []
                for row in url:
                    size = db.query(model.size).join(model.product_room_size).join(model.tiles_photos).filter(
                        model.tiles_photos.prs_id == row.prs_id
                    ).first()
                    ls = {
                        "size": size.sizes,
                        "url": row.photo_address
                    }
                    details.append(ls)
                return details
            if not product and not room and not size:
                url = db.query(model.tiles_photos).all()
                details = []
                for row in url:
                    size = db.query(model.size).join(model.product_room_size).join(model.tiles_photos).filter(
                        model.tiles_photos.prs_id == row.prs_id
                    ).first()
                    ls = {
                        "size": size.sizes,
                        "url": row.photo_address
                    }
                    details.append(ls)
                return details
        except Exception as e:
            return str(e)