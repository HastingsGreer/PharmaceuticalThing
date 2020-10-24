from flask import url_for, render_template, redirect
from flask import current_app as app
from .forms import  DemographicDataForm, DrugResponseDataForm


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
        print([q for q in dquestions])
        database_item = {
                q["name"]:getattr(form, q['name']).data
                for q in dquestions
        }
        #print(collection.insert_one(database_item))
        return redirect('/drugResponseData')
    return render_template('demographicData.jinja2',
                           form=form,
                           template='form-template')

@app.route('/drugResponseData', methods=('GET', 'POST'))
def drugResponseData():
    form = DrugResponseDataForm()
    if form.validate_on_submit():
        dquestions = questions["perDrugQuestions"]
        print([q for q in dquestions])
        database_item = {
                q["name"]:getattr(form, q['name']).data
                for q in dquestions
        }
        #print(collection.insert_one(database_item))
        print(form.submit)
        if form.submit.data: 
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
