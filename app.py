from flask import Flask, request, jsonify, render_template, abort, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from urllib.parse import ParseResult, quote

from flask_sqlalchemy.model import Model 


# from routes import api

app = Flask(__name__)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://admin:%s@172.20.0.5:5432/postgres" % quote("{{ dbpass }}")
app.config["SQLALCHEMY_POOL_RECYCLE"] = 10 # second to recycle the db connection

# init db
db = SQLAlchemy(app)
# init ma
ma = Marshmallow(app)

# app.register_blueprint(request_api.get_blueprint())

# app.register_blueprint(api)



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


# class for resustance table
class resistModel(db.Model):
    __tablename__ = "resustance"
    id = db.Column(db.Integer, primary_key=True)
    storedgrains = db.Column(db.Boolean, nullable=False)
    species = db.Column(db.String(100), nullable=False) # * species [fix the reference connection]
    # lifestage = db.Column(db.String(50))
    title = db.Column(db.String(300), nullable=False, unique=True) # * paper
    absent_present_aprd = db.Column(db.SmallInteger)
    chem_active = db.Column(db.String(75), nullable=False) # * chems
    resistance = db.Column(db.SmallInteger, nullable=False)
    severity = db.Column(db.String(50))
    # crop = db.Column(db.String(50))
    # state = db.Column(db.String(25))
    locality = db.Column(db.String(50))
    long = db.Column(db.Numeric(precision=6, scale=3))
    lat = db.Column(db.Numeric(precision=6, scale=3))
    # collect_year = db.Column(db.Integer)
    # chcek_point = db.Column(db.Data)

    def __init__(self, id, storedgrains, species, 
    title, absent_present_aprd, chem_active, 
    resistance, severity, locality,
    long, lat): # [lifestage, crop, state, collect_year, chcek_point]
        self.id = id
        self.storedgrains = storedgrains
        self. species = species
        # self.lifestage = lifestage
        self.title = title
        self.absent_present_aprd = absent_present_aprd
        self.chem_active = chem_active
        self.resistance = resistance
        self.severity = severity
        # self.crop = crop
        # self.state = state
        self.locality = locality
        self.long = long
        self.lat = lat
        # self.collect_year = collect_year
        # self.chcek_point = chcek_point



# create schema for the tables
# allowed feild to show on the get requests
class ChemSchema(ma.Schema):
	class Meta:
		fields = ("chem_active", "chem_group", "chem_irac")
# init schema
chem_schema = ChemSchema(many=False)
chems_schema = ChemSchema(many=True)

# schema for paper table
class PaperSchema(ma.Schema):
    class Meta:
        fields = ("author", "year", "title", "journal", "doi")
# init schema
paper_schema = PaperSchema(many=False)
papers_schema = PaperSchema(many=True)

# schema for species
class SpeciesSchema(ma.Schema):
    class Meta:
        fields = ("species",) # to create a tuple with only one item, you have to add a comma after the item
# init schema
sp_schema = SpeciesSchema(many=False)
sps_schema = SpeciesSchema(many=True)



# define the get requests
@app.route("/")
@app.route("/api")
@app.route("/api/")
def home():
    return redirect(url_for("get_docs")) # re-direct to docs

@app.route("/api/docs")
def get_docs():
    print("sending docs")
    return render_template("swaggerui.html")



# get request with schema
@app.route("/api/chems/all", methods=["GET"])
def get_chems():
	all_chems = chemsModel.query.all()
	result = chems_schema.dump(all_chems)
	return jsonify(result)


@app.route("/api/chems/id=<int:id>", methods=["GET"])
def get_chem(id):
    chembyid = chemsModel.query.get(id)
    if chembyid is None:
        abort(404, 
            description = "The selected id was not found!"
        )
    return chem_schema.jsonify(chembyid)


@app.route("/api/chems/active=<query>", methods=["GET"])
def chem_by_active(query):
	search = "%{}%".format(query)
	chemQuery = chemsModel.query.filter(chemsModel.chem_active.like(search)).all()
	if len(chemQuery) < 1:
		abort(404, 
			description = "No active similar to {} was found!".format(str(query))
		)
	result = chems_schema.dump(chemQuery)
	return jsonify(result)



@app.route("/api/species/all", methods=["GET"])
def species_list():
    allspecies = speciesModel.query.all()
    result = sps_schema.dump(allspecies)
    return jsonify(result)

@app.route("/api/species/id=<int:id>", methods=["GET"])
def get_species(id):
    speciesbyid = speciesModel.query.get(id)
    if speciesbyid is None:
        abort(404, 
            description = "The selected id was not found!"
        )
    return sp_schema.jsonify(speciesbyid)

@app.route("/api/species/name=<query>", methods=["GET"])
def sp_by_name(query):
    search = "%{}%".format(query)
    speciesQuery = speciesModel.query.filter(speciesModel.species.like(search)).all()
    if len(speciesQuery) < 1:
        abort(404, 
            description = "No species name similar to {} was found!".format(str(query))
        )
    result = sps_schema.dump(speciesQuery)
    return jsonify(result)


if __name__ == "__main__":
	app.run(host="0.0.0.0", port=5000, debug=True)
