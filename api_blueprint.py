
from flask import Blueprint, jsonify, render_template, abort, redirect, url_for

api = Blueprint("api", __name__, static_folder="static", template_folder="template")

# import database connections/models from app.py
from app import *


# define the get requests
@api.route("/")
@api.route("/api")
@api.route("/api/")
def home():
    return redirect(url_for("api.get_docs")) # re-direct to docs

@api.route("/api/docs")
def get_docs():
    print("sending docs")
    return render_template("swaggerui.html")



# get request with schema
@api.route("/api/chems/all", methods=["GET"])
def get_chems():
	all_chems = chems_table.query.all()
	result = chems_schema.dump(all_chems)
	return jsonify(result)


@api.route("/api/chems/id=<int:id>", methods=["GET"])
def get_chem(id):
    chembyid = chems_table.query.get(id)
    if chembyid is None:
        abort(404, 
            description = "The selected id was not found!"
        )
    return chem_schema.jsonify(chembyid)


## **** add more filter here *********
@api.route("/api/chems/active=<query>", methods=["GET"])
def chem_by_active(query):
	search = "%{}%".format(query)
	chemQuery = chems_table.query.filter(chems_table.chem_active.like(search)).all()
	if len(chemQuery) < 1:
		abort(404, 
			description = "No active similar to {} was found!".format(str(query))
		)
	result = chems_schema.dump(chemQuery)
	return jsonify(result)



@api.route("/api/species/all", methods=["GET"])
def species_list():
    allspecies = species_table.query.all()
    result = sps_schema.dump(allspecies)
    return jsonify(result)

@api.route("/api/species/id=<int:id>", methods=["GET"])
def get_species(id):
    speciesbyid = species_table.query.get(id)
    if speciesbyid is None:
        abort(404, 
            description = "The selected id was not found!"
        )
    return sp_schema.jsonify(speciesbyid)

@api.route("/api/species/name=<query>", methods=["GET"])
def sp_by_name(query):
    search = "%{}%".format(query)
    speciesQuery = species_table.query.filter(species_table.species.like(search)).all()
    if len(speciesQuery) < 1:
        abort(404, 
            description = "No species name similar to {} was found!".format(str(query))
        )
    result = sps_schema.dump(speciesQuery)
    return jsonify(result)


# @api.route("/api/resistance/all", methods=["GET"])
# def resist_list():
#     allresist = resist_table.query.all()
#     result = resists_schema.dump(allresist)
#     return jsonify(result)

@api.route("/api/resistance/id=<int:id>", methods=["GET"])
def get_resist(id):
    resistbyid = resist_table.query.get(id)
    if resistbyid is None:
        abort(404, 
            description = "The selected id was not found!"
        )
    return resist_schema.jsonify(resistbyid)

## **** add more filter here *********
@api.route("/api/resistance/locality=<query>", methods=["GET"])
def resist_filter(query):
    search = "%{}%".format(query)
    resistQuery = resist_table.query.filter(resist_table.locality.like(search)).all()
    if len(resistQuery) < 1:
        abort(404, 
            description = "No resistance with locality similar to {} was found!".format(str(query))
        )
    result = resists_schema.dump(resistQuery)
    return jsonify(result)
