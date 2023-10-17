from db.model import app
from graniteandmarbles.routes import grrouter
from sanitaryandfittings.routes import firouter
from tiles.routes import tirouter
from usersdir.routes import router
from usersdir import create_owner
from trends.routes import trendrouter
from finishes.routes import finishrouter

create_owner()

app.register_blueprint(grrouter)
app.register_blueprint(firouter)
app.register_blueprint(tirouter)
app.register_blueprint(router)
app.register_blueprint(trendrouter)
app.register_blueprint(finishrouter)


if __name__ == "__main__":
    app.run(debug = True)