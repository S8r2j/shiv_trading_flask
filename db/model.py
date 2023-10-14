from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from core.config import settings

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]= f"mysql+pymysql://{settings.DATABASE_USER}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOST}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}?charset=utf8"
db = SQLAlchemy(app)


class user(db.Model):
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    email = db.Column(db.String(100), nullable=True, unique=True)
    countrycode=db.Column(db.String(5), nullable=False)
    phonenumber = db.Column(db.String(11), unique=True, nullable=False)
    plan=db.Column(db.String(20),nullable=False)
    issuperuser=db.Column(db.Boolean, default = False)
    login = db.relationship('login', backref = 'user', lazy=True)


class login(db.Model):
    sn=db.Column(db.Integer,autoincrement=True,primary_key=True)
    id=db.Column(db.Integer,db.ForeignKey("user"),nullable=False)
    password=db.Column(db.String(250),nullable=False)


class products(db.Model):
    pid=db.Column(db.Integer, autoincrement=True, primary_key=True)
    productname=db.Column(db.String(100), nullable=False)


class sizes(db.Model):
    sid=db.Column(db.Integer, autoincrement=True, primary_key=True)
    sizes=db.Column(db.Text,nullable=False)


class rooms(db.Model):
    roomid=db.Column(db.Integer, nullable=False, primary_key=True)
    roomname=db.Column(db.String(100),nullable=False)


class cpfittings(db.Model):
    fittingid=db.Column(db.Integer, primary_key=True)
    fittingname=db.Column(db.String(100), nullable=False)


class productroomsize(db.Model):
    prsid=db.Column(db.Integer, autoincrement=True, primary_key=True)
    pid=db.Column(db.Integer, db.ForeignKey("products"))
    roomid=db.Column(db.Integer, db.ForeignKey("rooms"))
    sid=db.Column(db.Integer, db.ForeignKey("sizes"))
    tilesphotos=db.relationship('tilesphotos', backref='connection', lazy=True)


class tilesphotos(db.Model):
    photoid=db.Column(db.Integer,primary_key = True)
    photoaddress=db.Column(db.Text,nullable = False,unique = True)
    prsid=db.Column(db.Integer, db.ForeignKey('productroomsize'))


class productfitting(db.Model):
    pfittingid=db.Column(db.Integer,primary_key=True)
    pid=db.Column(db.Integer,db.ForeignKey("products"))
    fittingid=db.Column(db.Integer,db.ForeignKey("cpfittings"))
    photoaddress=db.relationship('cpphotos', backref='productfitting', lazy=True)


class cpphotos(db.Model):
    cpid=db.Column(db.Integer,primary_key = True)
    photoaddress=db.Column(db.Text,nullable = False)
    pfittingid=db.Column(db.Integer,db.ForeignKey("productfitting"))


class granites(db.Model):
    graniteid=db.Column(db.Integer,autoincrement = True,primary_key = True)
    category=db.Column(db.String(100),nullable = False)


class thick(db.Model):
    thickid=db.Column(db.Integer,autoincrement = True,primary_key = True)
    thick=db.Column(db.String(50),nullable = False)


class granitethick(db.Model):
    gtid=db.Column(db.Integer,autoincrement = True,primary_key = True)
    graniteid=db.Column(db.Integer,db.ForeignKey("granites"))
    thickid=db.Column(db.Integer,db.ForeignKey("thick"))
    pid=db.Column(db.Integer,db.ForeignKey("products"))
    photoaddress=db.relationship('granitephoto', backref='granitethick', lazy=True)


class granitephoto(db.Model):
    gpid=db.Column(db.Integer,autoincrement = True,primary_key = True)
    photoaddress=db.Column(db.Text,nullable = False)
    gtid=db.Column(db.Integer,db.ForeignKey("granitethick"))


class trendingproduct(db.Model):
    tpid=db.Column(db.Integer,autoincrement = True,primary_key = True)
    photoaddress=db.Column(db.Text,nullable = False)


class basicfinish(db.Model):
    bfid=db.Column(db.Integer,autoincrement = True,primary_key = True)
    photoaddress=db.Column(db.Text,nullable = False)


class standardfinish(db.Model):
    sfid=db.Column(db.Integer,autoincrement = True,primary_key = True)
    photoaddress=db.Column(db.Text,nullable = False)


class premiumfinish(db.Model):
    pfid=db.Column(db.Integer,autoincrement = True,primary_key = True)
    photoaddress=db.Column(db.Text,nullable = False)


with app.app_context():
    db.create_all()
    product = products.query.first()
    if not product:
        from sqlalchemy.sql import text
        with open("db/data.sql", 'r', encoding = 'utf-8') as sql_file:
            sql_commands = sql_file.read().split(';')
            for command in sql_commands:
                if command.strip():
                    stmt = text(command)
                    db.session.execute(stmt)

        db.session.commit()