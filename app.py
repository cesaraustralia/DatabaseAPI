from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from urllib.parse import quote
from sqlalchemy import ForeignKey


# import blueprint of routes
from api_blueprint import api

app = Flask(__name__)
app.register_blueprint(api, url_prefix="") # register bluprint
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://admin:%s@172.20.0.5:5432/postgres" % quote("{{ dbpass }}")
app.config["SQLALCHEMY_POOL_RECYCLE"] = 10 # second to recycle the db connection

# init db
db = SQLAlchemy(app)
# init ma
ma = Marshmallow(app)



# class for chem table
class chems_table(db.Model):
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
class species_table(db.Model):
    __tablename__ = "species"
    id = db.Column(db.Integer, primary_key=True)
    species = db.Column(db.String(100), nullable=False)
    # common_name = db.Column(db.String(200))
    # family = db.Column(db.String(100))
    # order = db.Column(db.String(100))
    # group = db.Column(db.String(50))
    # host = db.Column(db.String(50))

    def __init__(self, id, species): ## common_name, family, order, group, host
        self.id = id
        self.species = species
        # self.common_name = common_name
        # self.family = family
        # self.order = order
        # self.group = group
        # self.host = host


# class for paper table
class papers_table(db.Model):
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
class resist_table(db.Model):
    __tablename__ = "resistance"
    id = db.Column(db.Integer, primary_key=True)
    storedgrains = db.Column(db.Boolean, nullable=False)
    species = db.Column(db.String(100), ForeignKey("species_table.species"), nullable=False)
    # lifestage = db.Column(db.String(50))
    title = db.Column(db.String(300), ForeignKey("papers_table.title"), nullable=False)
    absent_present_aprd = db.Column(db.SmallInteger)
    active = db.Column(db.String(75), ForeignKey("chems_table.chem_active"), nullable=False)
    resistance = db.Column(db.SmallInteger, nullable=False)
    severity = db.Column(db.String(50))
    # crop = db.Column(db.String(50))
    # state = db.Column(db.String(25))
    locality = db.Column(db.String(50))
    long = db.Column(db.Numeric(precision=6, scale=3))
    lat = db.Column(db.Numeric(precision=6, scale=3))
    # collect_year = db.Column(db.Integer)
    # chcek_point = db.Column(db.Data)

    def __init__(self, id, storedgrains, species, title, absent_present_aprd, active, resistance, severity, locality, long, lat): # [lifestage, crop, state, collect_year, chcek_point]
        self.id = id
        self.storedgrains = storedgrains
        self.species = species
        # self.lifestage = lifestage
        self.title = title
        self.absent_present_aprd = absent_present_aprd
        self.active = active
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
    class Meta: ## "common_name", "family", "order", "group", "host"
        fields = ("species", ) # to create a tuple with only one item, you have to add a comma after the item
# init schema
sp_schema = SpeciesSchema(many=False)
sps_schema = SpeciesSchema(many=True)

# schema for resistance table
class ResistSchema(ma.Schema):
    class Meta:
        fields = ("storedgrains", "species", "title", "absent_present_aprd", "active", 
        "resistance", "severity", "locality", "long", "lat") # add the new ones when tables are updated
# init schema
resist_schema = ResistSchema(many=False)
resists_schema = ResistSchema(many=True)



if __name__ == "__main__":
	app.run(host="0.0.0.0", port=5000, debug=False)
