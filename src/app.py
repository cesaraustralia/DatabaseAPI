from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
# from flask_swagger_ui import get_swaggerui_blueprint
# from flask_restful import Api, abort
# from routes import request_api

app = Flask(__name__)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://admin:cesarau@172.20.0.5:5432/postgres"
# app.config["SQLALCHEMY_POOL_RECYCLE"] = 10 # second to recycle the db connection

db = SQLAlchemy(app)


# ## create swagger ui for api
# @app.route("/static/<path:path>")
# def send_static(path):
#     return send_from_directory("static", path)

# SWAGGER_URL = "/swagger"
# API_URL = "/static/swagger.json"
# SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
#     SWAGGER_URL,
#     API_URL,
#     config={
#         "app_name": "Cesar-WEB-API"
#     }
# )
# app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)

# app.register_blueprint(request_api.get_blueprint())


# class for chem table
class chemsModel(db.Model):
    __tablename__ = "chems"
    id = db.Column(db.Integer, primary_key=True)
    chem_active = db.Column(db.String(75), nullable=False)
    chem_group = db.Column(db.String(200), nullable=True)
    chem_irac = db.Column(db.String(5), nullable=True)

    def __init__(self, id, chem_active, chem_group, chem_irac):
        self.id = id
        self.chem_active = chem_active
        self.chem_group = chem_group
        self.chem_irac = chem_irac


# class for species table
class speciesModel(db.Model):
    __tablename__ = "species"
    id = db.Column(db.Integer, primary_key=True)
    species = db.Column(db.String(100), nullable=False)

    def __init__(self, id, species):
        self.id = id
        self.species = species


# class for paper table
class paperModel(db.Model):
    __tablename__ = "papers"
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(200), nullable=True)
    year = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(300), nullable=False, unique=True)
    journal = db.Column(db.String(200))
    doi = db.Column(db.String(200))

    def __init__(self, id, author, year, title, journal, doi):
        self.id = id
        self.author = author
        self.year = year
        self.title = title
        self.journal = journal
        self.doi = doi


## define the get requests
# @app.route("/")
# @app.route("/api")
# @app.route("/api/")
# def Main():
#     return "Welcome to the Cesar Australia API!"


# @app.route("/api/docs")
# def get_docs():
#     print("sending docs")
#     return render_template("swaggerui.html")


# @app.route('/')
# def get_root():
#     print('sending root')
#     return render_template('index.html')

@app.route('/api/docs')
def get_docs():
    print('sending docs')
    return render_template('swaggerui.html')

@app.route('/api')
def get_api():
    hello_dict = {'en': 'Hello', 'es': 'Hola'}
    lang = request.args.get('lang')
    return jsonify(hello_dict[lang])



@app.route("/api/chems", methods=["GET"])
def chem_list():
    allchems = chemsModel.query.all()
    output = []
    for ch in allchems:
        currChem = {}
        currChem["chem_active"] = ch.chem_active
        currChem["chem_group"] = ch.chem_group
        currChem["chem_irac"] = ch.chem_irac
        output.append(currChem)
    return jsonify(output)

@app.route("/api/chemId=<int:id>", methods=["GET"])
def chem_id(id):
    ch = chemsModel.query.filter(chemsModel.id == id).first_or_404(
        description = 'The id {} was not found!'.format(id)
    )
    output = {}
    output["chem_active"] = ch.chem_active
    output["chem_group"] = ch.chem_group
    output["chem_irac"] = ch.chem_irac
    return jsonify(output)


@app.route("/api/species", methods=["GET"])
def species_list():
    allspecies = speciesModel.query.all()
    output = []
    for sp in allspecies:
        currSp = {}
        currSp["id"] = sp.id
        currSp["species"] = sp.species
        output.append(currSp)
    return jsonify(output)


if __name__ == "__main__":
	app.run(host="0.0.0.0", port=5001, debug=True)
