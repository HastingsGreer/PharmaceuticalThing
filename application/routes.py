from flask import url_for, render_template, redirect, session
import os
from flask import current_app as app
from .forms import  DemographicDataForm, DrugResponseDataForm, VisualizationSettingsForm

from .plotting import serve_pil_image, make_plot

import tempfile
import pickle
import random
import pymongo

client = pymongo.MongoClient()
db = client.test_database
collection = db.LinksSubmitted


@app.route('/')
def home():
    return render_template('index.jinja2',
                           template='home-template')


import json
with open("questions.json") as q:
    questions = json.load(q)

@app.route('/demographicData', methods=('GET', 'POST'))
def demographicData():
    form = DemographicDataForm()
    if form.validate_on_submit():
        dquestions = questions["intakeQuestions"]
        database_item = {
                q["name"]:getattr(form, q['name']).data
                for q in dquestions
        }
        session["response_building"] = {
                "demographic_data": database_item,
                "drugs": []
        }
        
        return redirect('/drugResponseData')
    return render_template('demographicData.jinja2',
                           form=form,
                           template='form-template')

@app.route('/drugResponseData', methods=('GET', 'POST'))
def drugResponseData():
    form = DrugResponseDataForm()
    if form.validate_on_submit():
        dquestions = questions["perDrugQuestions"]
        database_item = {
                q["name"]:getattr(form, q['name']).data
                for q in dquestions
        }
        session["response_building"]["drugs"].append(database_item)
        session.modified = True
        if form.submit.data:
            #pickledb
            fname = "pickledb/" + str(random.random())[5:] + ".json"
            with open(fname, "w") as f:
                json.dump(session["response_building"], f)
            print(session["response_building"])
            return redirect("/success")
        if form.addAnotherDrug.data:
            return redirect("/drugResponseData")
    return render_template('drugResponseData.jinja2',
            form=form,
            template='form-template')

@app.route('/success', methods=('GET', 'POST'))
def success():
    return render_template('success.jinja2',
                           template='success-template')

@app.route('/plot', methods=('GET', 'POST'))
def plot():
    params = session["plot_params"]
    pil_image = make_plot(params)
    return serve_pil_image(pil_image)

@app.route('/visualization', methods=('GET', 'POST'))
def visualization():
    form = VisualizationSettingsForm()
    session["plot_params"] = {"x_var":"recommendation", "y_var":"drug", "drug": "Any","demo_filters":
       {q:getattr(form, q).default for q in form.my_formfields}
    }

    if form.validate_on_submit():
        session.modified=True
        plot_params = session["plot_params"]
        plot_params["x_var"] = form.x_var.data
        plot_params["y_var"] = form.y_var.data
        plot_params["drug"] = form.drug.data
        plot_params["demo_filters"] = {q:getattr(form, q).data for q in form.my_formfields}
    return render_template("visualization.jinja2", form=form, template='form-template', whoop=str(random.random())[5:])
@app.route('/annagraphs')
def annagraphs():
    fnames = os.listdir("application/static/annagraphs")
    return render_template("annagraphs.jinja2", fnames=["/annagraphs/" + f for f in sorted(fnames)], template='form-template')
@app.route('/patientResults')
def personal():
    fnames = os.listdir("application/static/patientResults")
    return render_template("patientResults.jinja2", fnames=["/patientResults/" + f for f in sorted(fnames)], template='form-template')
