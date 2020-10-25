import application.plotting

import application.forms

print(", ".join(q[0] for q in application.forms.questionNames))


demoQuestionNames = [q["name"] for q in application.forms.questions["intakeQuestions"]]
drugQuestionNames = [q["name"] for q in application.forms.questions["perDrugQuestions"]]


for r in application.plotting.responses:
    if application.plotting.data_valid(r, application.plotting.filters):
       for drug in r["drugs"]:
           
           print(", ".join(str(r["demographic_data"][name]) for name in demoQuestionNames), end=", ")
           print(", ".join(str(drug[name]) for name in drugQuestionNames))
