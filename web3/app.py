from flask import Flask, render_template
from mongoengine import *
import os
import csv
connect('Test')

app = Flask(__name__)
app.config.from_object('config')

class Country(Document):
	name = StringField()
	data = DictField()

@app.route('/loaddata')
def hello_world():
	for file in os.listdir(app.config['FILES_FOLDER']):
		filename = os.fsdecode(file)
		path = os.path.join(app.config['FILES_FOLDER'],filename)
		f = open(path)
		r = csv.DictReader(f)
		d = list(r)
		for data in d:
			#print(data)
			country = Country()
			dict = {}
			for key in data:

				if key == "country":

					if Country.objects(name = data[key]).count() == 0:
						country["name"] = data[key]

					else:
						country = Country.objects.get(name = data[key])
						dict = country["data"]

				else:
					f = filename.replace(".csv","")
					if f in dict:
						dict[f][key] = data[key]
					else:
						dict[f] = {key:data[key]}
	
				country["data"] = dict
			country.save()

	return 'Hello, World!'


@app.route('/test')
def test():
	title = "Page Title"
	myName = "Alister"
	NZ = Country(name='New Zealand')
	NZ.save()
	return render_template('page.html', name=myName, title=title)

@app.route('/')
def index():
	return 'Success!'

@app.route('/countries', methods=['GET'])
@app.route('/countries/<countries_id>', methods=['GET'])
def getCountries():
	countries = Country.objects



	return countries.to_json()










if __name__ =="__main__":
	app.run(debug=True, host='0.0.0.0', port=80)
