from flask import jsonify


def allowed_file(file):
    if file.filename == "":
        jsonify({"error": "File not found"}), 400
    allowed_extensions = ['jpg', 'jpeg', 'png', 'jfif']
    filename,extension = file.filename.lower().split('.')
    if extension not in allowed_extensions:
        jsonify({"error":"Image format should be of format jpg/jpeg/png/jfif"}), 415
    return True

# @app.route("/upload/trending/product/photos/",methods = ['POST'])
# async def upload_trending_photos(up_photo:UploadFile=File(...)):
#     usersdir = current_user
#     if not usersdir:
#         return jsonify({ "error": "User doesn't exist" }), 400
#     if not usersdir.issuperuser:
#         return jsonify({ "error": "User not authorized to modify" }), 401
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
# @router.post("/upload/finish/photos/",dependencies = [Depends(deps.get_current_user)])
# async def upload_finish_photos(plan:str,up_photo:UploadFile=File(...),db:Session=Depends(dbconnect.get_database),usersdir:model.usersdir=Depends(deps.get_current_user)):
#     usersdir = db.query(model.usersdir).filter(
#         model.usersdir.phone_number == usersdir.phone_number,
#         model.usersdir.is_superuser == True
#     ).first()
#     if not usersdir or not usersdir.is_superuser:
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