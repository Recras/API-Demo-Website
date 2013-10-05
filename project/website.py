from flask import Flask, render_template, request
import requests
import base64
import data

app = Flask(__name__)
app.config['RECRAS_URL'] = 'https://demo.recras.nl/'
app.config['RECRAS_CRT'] = 'project/recras.nl.crt'

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
		arrangement_data = data.arrangementen[arrangement['id']] if arrangement['id'] in data.arrangementen else None 
		return render_template('arrangement.html', arrangement = arrangement, data = arrangement_data)

@app.route('/producten')
def producten():
	url = '%s/api/json/producten/' % app.config['RECRAS_URL']
	r = requests.get(url, verify=app.config['RECRAS_CRT']).json()
	if r['succes']:
		producten = r['results']	
		return render_template('producten.html', producten = producten)

@app.route('/producten/<int:product_id>')
def product(product_id):
	url = '%s/api/json/producten/id/%i' % (app.config['RECRAS_URL'], product_id)
	r = requests.get(url, verify=app.config['RECRAS_CRT']).json()
	if r['succes']:
		product = r['results'][0]
		return render_template('product.html', product = product)

@app.route('/contactformulier')
def contactformulier():
	proxy = base64.urlsafe_b64encode('/proxy'.encode('utf-8'))
	redirect = base64.urlsafe_b64encode('/bedankt'.encode('utf-8'))
	url = "%s/api/json/contactformulier/proxy/%s/redirect/%s" % (app.config['RECRAS_URL'], proxy.decode("utf-8"), redirect.decode("utf-8"))
	r = requests.get(url, verify=app.config['RECRAS_CRT']).json()
	if r['succes']:
		return render_template('contactformulier.html', formulier = r['results'])

@app.route('/proxy', methods=['POST'])
def proxy():
	url = '%s/api/json/contactformulier' % app.config['RECRAS_URL']
	r = requests.post(url, data=request.form, verify=app.config['RECRAS_CRT'])
	return r.text

@app.route('/onlineboeken')
def onlineboeken():
	return render_template('onlineboeken.html')

@app.route('/bedankt')
def bedankt():
	return render_template('bedankt.html')

if __name__ == "__main__":
	app.debug = True
	app.run()
