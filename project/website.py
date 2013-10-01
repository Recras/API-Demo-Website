from flask import Flask, render_template, request
import requests

app = Flask(__name__)
app.config['RECRAS_URL'] = 'https://demo.recras.nl/'
app.config['RECRAS_CRT'] = 'recras.nl.crt'

@app.route('/')
def home():
	return render_template('home.html')

@app.route('/arrangementen')
def arrangementen():
	url = '%s/api/json/arrangementen/' % app.config['RECRAS_URL']
	r = requests.get(url, verify=app.config['RECRAS_CRT']).json()
	if r['succes']:
		arrangementen = r['results']	
		return render_template('arrangementen.html', arrangementen = arrangementen)

@app.route('/arrangementen/<int:arrangement_id>')
def arrangement(arrangement_id):
	url = '%s/api/json/arrangementen/id/%i' % (app.config['RECRAS_URL'], arrangement_id)
	r = requests.get(url, verify=app.config['RECRAS_CRT']).json()
	if r['succes']:
		arrangement = r['results'][0]	
		return render_template('arrangement.html', arrangement = arrangement)

@app.route('/producten')
def producten():
	url = '%s/api/json/producten/' % app.config['RECRAS_URL']
	r = requests.get(url, verify=app.config['RECRAS_CRT']).json()
	if r['succes']:
		producten = r['results']	
		return render_template('producten.html', producten = producten)

if __name__ == "__main__":
	app.debug = True
	app.run()
