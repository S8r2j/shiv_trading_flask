from flask import request, abort, Response, json
from db.model import db,app, products, sizes, rooms, tilesphotos, productroomsize, cpfittings, cpphotos, productfitting,granites,granitethick,granitephoto, thick

@app.route("/tiles/photos/", methods = ['GET'])
def get_tiles_photos():
    product = request.args.get('product', default = None, type = str)
    size = request.args.get('size', default = None, type = str)
    room = request.args.get('room', default = None, type = str)
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
                        details.append(ls)
                return Response(
                        json.dumps(details, ensure_ascii = False).encode('utf-8'),
                        content_type = 'application/json; charset=utf-8'
                        )
        except Exception as e:
            return str(e)


@app.route("/cpfittings/photos/", methods = ['GET'])
def get_cpfitting_photos():
    fittingname = request.args.get('fittingname', default = None, type = str)
    details = []
    with app.app_context():
        if not fittingname:
            photo = cpphotos.query.all()
            for row in photo:
                details.append(row.photoaddress)
        if fittingname:
            query=cpfittings.query.filter(cpfittings.fittingname == fittingname).first()
            if not query:
                abort(404)
            photo= productfitting.query.join(cpfittings).filter(cpfittings.fittingname == fittingname).all()
            for row in photo.photoaddress:
                details.append(row.photoaddress)

        return Response(
            json.dumps(details, ensure_ascii = False).encode('utf-8'), content_type = 'application/json; charset=utf-8'
            )


@app.route("/granite/photos/", methods = ['GET'])
def get_granite_photos():
    granite = request.args.get('granite', default = None, type = str)
    thik = request.args.get('thick', default = None, type = str)
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
            url = granitethick.query.join(granites).join(thick
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
                size = thick.query.join(granitephoto).filter(
                    granitephoto.gt_id == row.gt_id
                ).first()
                ls = {
                    "size": size.sizes,
                    "url": row.photoaddress
                }
                details.append(ls)
            return details
        if not granite and not thik:
            url = granitephoto.query.join(granitethick).all()
            details = []
            for row in url:
                size = thick.query.join(granitephoto).filter(
                    granitephoto.gt_id == row.gt_id
                ).first()
                ls = {
                    "size": size.sizes,
                    "url": row.photoaddress
                }
                details.append(ls)
            return details
    except Exception as e:
        return str(e)
