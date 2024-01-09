from db.model import app
from graniteandmarbles.routes import grrouter
from sanitaryandfittings.routes import firouter
from tiles.routes import tirouter
from usersdir.routes import router
from usersdir import create_owner
from trends.routes import trendrouter
from finishes.routes import finishrouter
from flask_cors import CORS
from flask import render_template
import json

CORS(app)

create_owner()

app.register_blueprint(grrouter)
app.register_blueprint(firouter)
app.register_blueprint(tirouter)
app.register_blueprint(router)
app.register_blueprint(trendrouter)
app.register_blueprint(finishrouter)

routes_dict = {}
first_iteration = True
for rule in app.url_map.iter_rules():
    if first_iteration:
        first_iteration = False
        continue
    endpoint = app.view_functions[rule.endpoint].__name__
    routes_dict[rule.rule] = endpoint.replace("_"," ")
@app.route("/", methods = ['GET'])
def welcome_page():
    return render_template('about.html', endpoints_data = routes_dict)


if __name__ == "__main__":
    app.run(debug = True)