import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import PIL
import os
import json
from io import BytesIO
from flask import send_file

responses = []

for f in os.listdir("pickledb"):
    with open("pickledb/" + f, "r") as ff:
	    responses.append(json.load(ff))

responses_flat = []

for res in responses:
    for drug in res["drugs"]:
        responses_flat.append({**res["demographic_data"], **drug})

def serve_pil_image(pil_img):
    img_io = BytesIO()
    pil_img.save(img_io, 'JPEG', quality=70)
    img_io.seek(0)
    return send_file(img_io, mimetype='image/jpeg')

def plot(x_key, y_key, filters=[]):
    xs = []
    ys = []
    for r in responses_flat:
        if data_valid(r, filters):
            xs.append(x_key(r))
            ys.append(y_key(r))
    plt.scatter(xs, ys)
    return PIL_show()

def data_valid(r, filters):
    for f in filters:
        if not(f(r)):
            return False
    return True

def PIL_show():
    canvas = plt.get_current_fig_manager().canvas
    canvas.draw()
    pil_image = PIL.Image.frombytes('RGB', canvas.get_width_height(), 
                 canvas.tostring_rgb())
    return pil_image


filters = [
    lambda x: "age" in x
]
def make_plot(params):
    plt.clf()
    x_var = params["x_var"]
    y_var = params["y_var"]
    drug = params["drug"]
    plt.xlabel(x_var)
    plt.ylabel(y_var)
    if drug != "Any":
        drug_filter = lambda x: x["drug"] == drug
    else:
        drug_filter = lambda x: True
    
    

    return plot(
        lambda x: x[x_var], 
        lambda x: x[y_var], filters + [drug_filter])




