from flask import url_for, render_template, redirect, session
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
    session["plot_params"] = {"x_var":"height", "y_var":"weight", "drug": "Any"}

    if form.validate_on_submit():
        session.modified=True
        plot_params = session["plot_params"]
        plot_params["x_var"] = form.x_var.data
        plot_params["y_var"] = form.y_var.data
        plot_params["drug"] = form.drug.data

    return render_template("visualization.jinja2", form=form, template='form-template')
