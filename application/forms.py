"""Form class declaration."""
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import (
                     SubmitField,
                     SelectField,
                     DecimalField,
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
        print("initted")
        self.my_formfields_bound = [getattr(self, f) for f in self.my_formfields]
        
    def bind(*args):
        super(DemographicDataForm, self).bind(*args)
        self.my_formfields_bound = []
        print("ierere")
        for name in self.my_formfields:
            self.my_formfields_bound.append(
                    getattr(self, name)
            )
            print(name)


for demoq in questions['intakeQuestions']:
    if demoq["type"] == 'categorical':
        setattr(DemographicDataForm, demoq["name"], SelectField(demoq["question"], 
            choices = [(c, c) for c in demoq["categories"]]))
    if demoq["type"] == 'number':
        setattr(DemographicDataForm, demoq["name"], DecimalField(demoq["question"]))
    if demoq["type"] == 'boolean':
        setattr(DemographicDataForm, demoq["name"], BooleanField(demoq["question"]))
    DemographicDataForm.my_formfields.append( demoq["name"])
DemographicDataForm.submit = SubmitField('Next (Your results with specific drugs)')

