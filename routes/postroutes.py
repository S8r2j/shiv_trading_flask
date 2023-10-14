from flask import request, abort, Response, json, jsonify
import io
from db.model import db, products, sizes, rooms, tilesphotos, productroomsize, cpfittings, cpphotos, productfitting,granites,granitethick,granitephoto, thick
from routes import imagekit
from routes import upphoto
from routes.getroutes import app
from core.config import settings
from flask_sqlalchemy import SQLAlchemy
from PIL import Image
import imagekitio
import tempfile



def allowed_file(file):
    max_size = 10  # 10MB
    if file.filename == "":
        abort(404, description = "File not found")
    allowed_extensions = ['jpg', 'jpeg', 'png', 'jfif']
    filename,extension = file.filename.lower().split('.')
    if extension not in allowed_extensions:
        abort(415, description = "Image can be of jpg/jpeg/png/jfif formats only")
    return True

@app.route('/upload/tiles/photos/', methods=['POST'])
def upload_photo():
    product = request.args.get('product', type = str)
    size = request.args.get('size', type = str)
    room = request.args.get('room', type = str)
    ## Get the unique number for each of the products
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
    ## Got the unique number

    file = request.files['up_photo']
    if allowed_file(file):
            # Get the URL of the uploaded image
        image_url = upphoto.upload_photo(file,"tiles")
        photo_address = image_url
        with app.app_context():
            upload_photo = tilesphotos(photoaddress = photo_address, prsid = tile_type.prsid)
            db.session.add(upload_photo)
            db.session.commit()

        return { "message": "Photo uploaded successfully" }


@app.route("/upload/cpfittings/photos/", methods=['POST'])
def upload_cpfittings_photos():
    product = request.args.get('product', type = str)
    fitting_name = request.args.get('fitting_name', type = str)

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

    up_photo = request.files['up_photo']
    if allowed_file(up_photo):

        # Get the URL of the uploaded image
        image_url = upphoto.upload_photo(up_photo, "cpphotos")
        photo_address = image_url
        with app.app_context():
            upload_photo = cpphotos(photoaddress = photo_address, pfittingid = tile_type.pfittingid)
            db.session.add(upload_photo)
            db.session.commit()
            db.session.refresh(upload_photo)

        return { "message": "Photo uploaded successfully" }


@app.route("/upload/granite&marble/photos/", methods=['POST'])
def upload_granite_photos():
    product = request.args.get('product', type = str)
    granite = request.args.get('granite', type = str)
    thik = request.args.get('thick', type = str)
    query = products.query.filter(products.productname == product).first()
    if not query:
        abort(404, description = "No such product found")

    query = granites.query.filter(granites.category == granite).first()
    if not query:
        abort(404, description = "No such category of granites item found")

    tile_type = granitethick.query.join(products).join(granites).join(thick).filter(
        products.productname == product
    ).filter(products.productname==product).filter(granites.category==granite).filter(
        thick.thick==thik
    ).first()

    file = request.files["up_photo"]
    if allowed_file(file = file):

        # Get the URL of the uploaded image
        image_url = upphoto.upload_photo(file, "granitephotos")
        photo_address = image_url
        with app.app_context():
            upload_photo = granitephoto(photoaddress = photo_address, gtid=tile_type.gtid)
            db.session.add(upload_photo)
            db.session.commit()
            db.session.refresh(upload_photo)

    return { "message": "Photo uploaded successfully" }


# @router.post("/upload/trending/product/photos/",dependencies = [Depends(deps.get_current_user)])
# async def upload_trending_photos(up_photo:UploadFile=File(...),user:model.user=Depends(deps.get_current_user),db:Session=Depends(dbconnect.get_database)):
#     user = db.query(model.user).filter(
#         model.user.phone_number == user.phone_number,
#         model.user.is_superuser == True
#     ).first()
#     if not user or not user.is_superuser:
#         raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = "Unauthorized attempt to make changes")
#
#     validate_photo(up_photo)
#     image_data = await up_photo.read()
#
#     # Upload the image to ImageKit
#     upload_response = imagekit.upload_file(
#         file = io.BytesIO(image_data),
#         file_name = "trending product",
#         options = { "folder": "/trending_product/" }
#     )
#     # Get the URL of the uploaded image
#     image_url = upload_response.get("response")
#     image_url = image_url.get("url")
#     photo_address = image_url
#     upload_photo = model.TrendingProduct(photo_address = photo_address)
#     db.add(upload_photo)
#     db.commit()
#     db.refresh(upload_photo)
#
#     return { "message": "Photo uploaded successfully",
#              "photo url":photo_address
#              }
#
#
# @router.post("/upload/finish/photos/",dependencies = [Depends(deps.get_current_user)])
# async def upload_finish_photos(plan:str,up_photo:UploadFile=File(...),db:Session=Depends(dbconnect.get_database),user:model.user=Depends(deps.get_current_user)):
#     user = db.query(model.user).filter(
#         model.user.phone_number == user.phone_number,
#         model.user.is_superuser == True
#     ).first()
#     if not user or not user.is_superuser:
#         raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = "Unauthorized attempt to make changes")
#     validate_photo(up_photo)
#
#     if plan=="Basic":
#         image_data = await up_photo.read()
#
#         # Upload the image to ImageKit
#         upload_response = imagekit.upload_file(
#             file = io.BytesIO(image_data),
#             file_name = "shivtrading_basic",
#             options = { "folder": "/basic_finish/" }
#         )
#         # Get the URL of the uploaded image
#         image_url = upload_response.get("response")
#         image_url = image_url.get("url")
#         photo_address = image_url
#         basic=model.BasicFinish(photo_address=photo_address)
#         db.add(basic)
#         db.commit()
#         db.refresh(basic)
#     if plan=="Standard":
#         image_data = await up_photo.read()
#
#         # Upload the image to ImageKit
#         upload_response = imagekit.upload_file(
#             file = io.BytesIO(image_data),
#             file_name = "shivtrading_standard",
#             options = { "folder": "/standard_finish/" }
#         )
#         # Get the URL of the uploaded image
#         image_url = upload_response.get("response")
#         image_url = image_url.get("url")
#         photo_address = image_url
#         standard=model.StandardFinish(photo_address=photo_address)
#         db.add(standard)
#         db.commit()
#         db.refresh(standard)
#     if plan=="Premium":
#         image_data = await up_photo.read()
#
#         # Upload the image to ImageKit
#         upload_response = imagekit.upload_file(
#             file = io.BytesIO(image_data),
#             file_name = "shivtrading_premium",
#             options = { "folder": "/premium_finish/" }
#         )
#         # Get the URL of the uploaded image
#         image_url = upload_response.get("response")
#         image_url = image_url.get("url")
#         photo_address = image_url
#         premium=model.PremiumFinish(photo_address=photo_address)
#         db.add(premium)
#         db.commit()
#         db.refresh(premium)
#     return "Photo added successfully"