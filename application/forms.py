"""Form class declaration."""
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import (
                     SubmitField,
                     SelectField,
                     FloatField,
                     BooleanField)
from wtforms.validators import (DataRequired,
                                EqualTo,
                                Length,
                                URL)


import json

with open("questions.json") as q:
    questions = json.load(q)

class DemographicDataForm(FlaskForm):
    """Demographic Data form."""
    my_formfields = []
    def __init__(self):
        super(DemographicDataForm, self).__init__()
        self.my_formfields_bound = [getattr(self, f) for f in self.my_formfields]


for demoq in questions['intakeQuestions']:
    if demoq["type"] == 'categorical':
        setattr(DemographicDataForm, demoq["name"], SelectField(demoq["question"], 
            choices = [(c, c) for c in demoq["categories"]]))
    if demoq["type"] == 'number':
        setattr(DemographicDataForm, demoq["name"], FloatField(demoq["question"]))
    if demoq["type"] == 'boolean':
        setattr(DemographicDataForm, demoq["name"], BooleanField(demoq["question"]))
    DemographicDataForm.my_formfields.append( demoq["name"])
DemographicDataForm.submit = SubmitField('Next (Your results with specific drugs)')

class DrugResponseDataForm(FlaskForm):
    "Drug response form"
    my_formfields = []
    def __init__(self):
        super(DrugResponseDataForm, self).__init__()
        self.my_formfields_bound = [getattr(self, f) for f in self.my_formfields]

for drugq in questions["perDrugQuestions"]:
    if drugq["type"] == 'categorical':
        setattr(DrugResponseDataForm, drugq["name"], SelectField(drugq["question"], 
            choices = [(c, c) for c in drugq["categories"]]))
    if drugq["type"] == 'number':
        setattr(DrugResponseDataForm, drugq["name"], FloatField(drugq["question"]))
    if drugq["type"] == 'boolean':
        setattr(DrugResponseDataForm, drugq["name"], BooleanField(drugq["question"]))
    DrugResponseDataForm.my_formfields.append( drugq["name"])

DrugResponseDataForm.submit = SubmitField('Submit')
DrugResponseDataForm.addAnotherDrug = SubmitField('Add Another Drug')


demoQuestions = questions["intakeQuestions"]
drugQuestions = questions["perDrugQuestions"]
allQuestions = demoQuestions + drugQuestions

questionNames = [(q["name"], q["name"]) for q in allQuestions]
drugs = questions["perDrugQuestions"][0]["categories"]
class VisualizationSettingsForm(FlaskForm):
    drug = SelectField("Drug or Category to investigate", 
        choices=[("Any", "Any")] + [(d, d) for d in drugs])
    x_var = SelectField("'Independent' Variable", choices=questionNames, default="weight")
    y_var = SelectField("'Dependent' Variable", choices=questionNames, default="nausea")
    submit = SubmitField("Update Chart")

    my_formfields = []
    def __init__(self):
        super(VisualizationSettingsForm, self).__init__()
        self.my_formfields_bound = [getattr(self, f) for f in self.my_formfields]

for demoq in questions["intakeQuestions"]:
    if demoq["type"] == 'categorical':
        setattr(VisualizationSettingsForm, demoq["name"], SelectField("Filter by " + demoq["name"], 
            choices = [("Any", "Any")] + [(c, c) for c in demoq["categories"]][1:]))
        VisualizationSettingsForm.my_formfields.append( demoq["name"] )
    if demoq["type"] == 'number':
        setattr(VisualizationSettingsForm, demoq["name"] + "_min", FloatField("Minimum " +  demoq["name"], default=0))
        setattr(VisualizationSettingsForm, demoq["name"] + "_max", FloatField("Maximum " +  demoq["name"], default=999))
        VisualizationSettingsForm.my_formfields.append( demoq["name"] + "_min")
        VisualizationSettingsForm.my_formfields.append( demoq["name"] + "_max")
