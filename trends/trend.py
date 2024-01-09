from db.model import trendingproduct, db, app, tilesphotos, cpphotos, granitephoto
from flask import Response, json, jsonify
from flask_jwt_extended import jwt_required, current_user


class Trending:
    def get_trending_products(self):
        query = trendingproduct.query.all()
        trend_product = []
        tiles = tilesphotos.query.all()
        query = db.session.query(tilesphotos, trendingproduct).filter(tilesphotos.photoaddress == trendingproduct.photoaddress)
        # Execute the query to retrieve the matching rows
        results = query.all()
        for tile,trend in results:
            ls = {
                "url":trend.photoaddress
            }
            if tile.description:
                ls["description"]=tile.description
            trend_product.append(ls)
        query = db.session.query(cpphotos, trendingproduct).filter(cpphotos.photoaddress == trendingproduct.photoaddress).all()
        for cp,trend in query:
            ls = {
                "url":trend.photoaddress
            }
            if cp.description:
                ls["description"]=cp.description
            trend_product.append(ls)
        query = db.session.query(granitephoto, trendingproduct).filter(granitephoto.photoaddress == trendingproduct.photoaddress).all()
        for gr, trend in query:
            ls = {
                "url": trend.photoaddress
            }
            if gr.description:
                ls["description"] = gr.description
            trend_product.append(ls)
        return Response(json.dumps(trend_product, ensure_ascii=False).encode('utf-8'), content_type='application/json; charset=utf-8')

    @jwt_required()
    def post_trending_products(self, photourl):
        user = current_user
        if not user:
            return jsonify({ "error": "User doesn't exist" }), 400
        if not user.issuperuser:
            return jsonify({ "error": "User not authorized to modify" }), 401
        trending_photo = trendingproduct(photoaddress = photourl)
        try:
            with app.app_context():
                db.session.add(trending_photo)
                db.session.commit()
                db.session.refresh(trending_photo)
            return "Photo uploaded successfully"
        except Exception as e:
            return {"error":f"{str(e)}"}

    @jwt_required()
    def delete_trending_product(self, photourl):
        user = current_user
        if not user:
            return jsonify({ "error": "User doesn't exist" }), 400
        if not user.issuperuser:
            return jsonify({ "error": "User not authorized to modify" }), 401
        with app.app_context():
            product = trendingproduct.query.filter(trendingproduct.photoaddress == photourl).first()
            if product:
                db.session.delete(product)
                db.session.commit()
                return "Successfully removed from trending products"