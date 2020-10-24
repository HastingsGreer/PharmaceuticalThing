from flask import url_for, render_template, redirect
from flask import current_app as app
from .forms import  DemographicDataForm


import pymongo

client = pymongo.MongoClient()
db = client.test_database
collection = db.LinksSubmitted


@app.route('/')
def home():
    return render_template('index.jinja2',
                           template='home-template')


@app.route('/demographicData', methods=('GET', 'POST'))
def demographicData():
    form = DemographicDataForm()
    if form.validate_on_submit():
        print(collection.insert_one({
          "name":form.name.data,
          "notes":form.notes.data,
          "tag":form.tag.data,
          "link":form.link.data
          }))
        return redirect('/success')
    return render_template('demographicData.jinja2',
                           form=form,
                           template='form-template')


@app.route('/success', methods=('GET', 'POST'))
def success():
    return render_template('success.jinja2',
                           template='success-template')
