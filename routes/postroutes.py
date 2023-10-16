from flask import request, abort
from routes.getroutes import app
from db import tiles, fittings, granitemarbel
from flask_jwt_extended import jwt_required



def allowed_file(file):
    if file.filename == "":
        abort(404, description = "File not found")
    allowed_extensions = ['jpg', 'jpeg', 'png', 'jfif']
    filename,extension = file.filename.lower().split('.')
    if extension not in allowed_extensions:
        abort(415, description = "Image can be of jpg/jpeg/png/jfif formats only")
    return True



@app.route('/upload/tiles/photos/', methods=['POST'])
@jwt_required()
def upload_photo():
    product = request.args.get('product', type = str)
    size = request.args.get('size', type = str)
    room = request.args.get('room', type = str)

    file = request.files['up_photo']
    if allowed_file(file):
        tile = tiles.Tiles(product = product, room = room, size = size, file = file)
        response = tile.post_tiles()
        return response




@app.route("/upload/cpfittings/photos/", methods=['POST'])
@jwt_required()
def upload_cpfittings_photos():
    product = request.args.get('product', type = str)
    fitting_name = request.args.get('fitting_name', type = str)
    up_photo = request.files['up_photo']
    if allowed_file(up_photo):
        fitting = fittings.Sanitary(product = product, fitting_name = fitting_name, file = up_photo)
        response = fitting.post_fittings()
        return response




@app.route("/upload/granite&marble/photos/", methods=['POST'])
@jwt_required()
def upload_granite_photos():
    product = request.args.get('product', type = str)
    granite = request.args.get('granite', type = str)
    thik = request.args.get('thick', type = str)
    file = request.files["up_photo"]

    if allowed_file(file = file):
        gr = granitemarbel.Marbles(product = product, granite = granite, thik = thik, file = file)
        response = gr.post_granites()
        return response




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