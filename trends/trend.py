from db.model import trendingproduct, db, app
from flask import Response, json, jsonify
from flask_jwt_extended import jwt_required, current_user


class Trending:
    def get_trending_products(self):
        query = trendingproduct.query.all()
        trend_product = []
        for row in query:
            trend_product.append(row.photoaddress)
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