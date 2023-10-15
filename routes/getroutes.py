from flask import request
from db.model import app
from db import tiles, fittings, granitemarbel



@app.route("/tiles/photos/", methods = ['GET'])
def get_tiles_photos():
    product = request.args.get('product', default = None, type = str)
    size = request.args.get('size', default = None, type = str)
    room = request.args.get('room', default = None, type = str)
    tile = tiles.Tiles(product = product, size = size, room = room)
    response = tile.get_tiles()
    return response



@app.route("/cpfittings/photos/", methods = ['GET'])
def get_cpfitting_photos():
    fittingname = request.args.get('fittingname', default = None, type = str)
    fitting = fittings.Sanitary(fitting_name = fittingname)
    response = fitting.get_fittings()
    return response



@app.route("/granite/photos/", methods = ['GET'])
def get_granite_photos():
    granite = request.args.get('granite', default = None, type = str)
    thik = request.args.get('thick', default = None, type = str)
    gr = granitemarbel.Marbles(granite = granite, thik = thik)
    response = gr.get_granites()
    return response