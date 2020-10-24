# PharmaceuticalThing
```
git clone https://github.com/HastingsGreer/PharmaceuticalThing
cd PharmaceuticalThing
conda create -n pharmathing python=3.7
conda activate pharmathing
conda install pip
pip install -r requirements.txt
```
Create a file name .env with one line in it:
```
SECRET_KEY=<INSERT GIBBERISH HERE>
```
run the app with 
```
flask run
```
then go to localhost:5000 in your browser
