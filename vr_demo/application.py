# coding: utf-8
from functools import wraps
from flask import Flask, render_template,url_for,redirect,request,make_response,flash,jsonify,g
import boto3
from flask_mobility import Mobility
from flask_mobility.decorators import mobile_template,mobilized
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, SubmitField, RadioField,SelectField
from wtforms import validators, ValidationError
from flask_mail import Mail,  Message
import json
import jwt
from jwt.contrib.algorithms.pycrypto import RSAAlgorithm
import stripe
import os
import pprint

# use the stripe keys to handle the payment
stripe_keys = {
  'secret_key': os.getenv('SECRET_KEY'),
  'publishable_key': os.getenv('PUBLISHABLE_KEY')
}
stripe.api_key = stripe_keys['secret_key']

application = Flask(__name__, template_folder="templates")
application.secret_key = 'development key'
Mobility(application)
s3 = boto3.resource('s3')
s3_bucket_name = 'vr-content'
vr_s3_folder = 'https://s3.us-east-2.amazonaws.com/vr-content/'
bucket = s3.Bucket(s3_bucket_name)

class ContactForm(FlaskForm):
    name = StringField("Contact")
    email = StringField("Email")
    phone = StringField("Phone")
    size = SelectField('Size of Space', choices=[('200 sq.m. or less ', '200 sq.m. or less'),
                                                 ('200-500 sq.m.', '200-500 sq.m.'),
                                                 ('> 500 sq.m.', '> 500 sq.m.'),
                                                 ('> 1000 sq.m.', '> 1000 sq.m.')])
    type = SelectField('Property Type', choices=[('Single Family ','Single Family'),
                                                 ('Condo','Condo'),
                                                 ('Commercial','Commercial'),
                                                 ('Retail','Retail'),
                                                 ('Boat','Boat'),
                                                 ('Aircraft','Aircraft')])
    date = SelectField('Date Needed', choices=[('1-2 days ','1-2 days'),
                                               ('1-4 days','1-4 days'),
                                               ('1-7 days','1-7 days'),
                                               ('7-14 days','7-14 days'),
                                               ('no preference','no preference')])
    submit = SubmitField("Submit Request")

class CreditForm(FlaskForm):
    subscribe_amount = StringField("Topup Amount($NZD):")
    submit = SubmitField("Credit Account")

mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": 'abinlaa@gmail.com',
    "MAIL_PASSWORD": 'Sp-3308897'
}
pem = '-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAh3pj5bpRO8AceRRe8QXn\n3p0Il0G+Mfky4UyuhtPQHCbcLnQIi8JL2v0qAgf41GaW8+sCylpmKdyVCbG20yde\nRpIBzw6+Ni2J4/MBuL5WAwwqhNIjPjNZxzVkGG/fYY5cPNXSsET1HzWAai/kU9DV\n2KLetvUQFzcJtmZWKvQ6SDD8AQo4wUAm/HqSQ66bFanKEvNaqwAGH95SFKgqdT9b\n0ZEZZzG0QBjlx8fpQPIdwJqhduBjQBv9KBNNDHXVNSOIe9ZFFWJ/NBURRp+H+6xa\nL8lGU6/MRFv4OwPYn5kLVuSj/Tm1wNegDcpGNcjuBZ4fyDe7sAvA1g4RJZ0Vdln2\neQIDAQAB\n-----END PUBLIC KEY-----\n'

application.config.update(mail_settings)
mail = Mail(application)

# use PEM to validate the token
def is_token_valid(token):
    try:
        decoded_token = jwt.decode(token, pem, algorithms=['RS256'])
        iss = 'https://cognito-idp.us-east-2.amazonaws.com/us-east-2_kRoPjEqA4'
        if decoded_token['iss'] != iss:
            return False
        elif decoded_token['token_use'] != 'access':
            return False
        return True
    except Exception:
        return False
#
def validate_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if kwargs['token'] == None or is_token_valid(kwargs['token'])==False:
            return print("invalide token, need to login")
        return f(*args, **kwargs)
    return decorated_function


@application.route("/fetch_vr/<string:place_id>")
def fetch_vr(place_id):
    return render_template("3dspace.html",name="JGPnGQ6hosj")

@application.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

# @application.route("/vrservice")
# def vr_service():
#     return render_template("vrservice.html")

@application.route("/contact", methods = ['GET', 'POST'])
def contact():
    form = ContactForm()
    if request.method == 'POST':
        if form.validate() == False:
            flash('All fields are required.')
            return render_template('contact.html', form=form)
        else:
            with application.app_context():
                msg = Message(subject="Quotation Received from {}".format(form.data['name']),
                              sender=application.config.get("MAIL_USERNAME"),
                              recipients=[form.data['email']],  # replace with your email for testing
                              body=json.dumps(form.data))
                mail.send(msg)
            flash('Quote request received, We will contact you shortly!')
            return redirect("/", code=302)
    elif request.method == 'GET':
        return render_template('contact.html', form=form)

@application.route("/price")
def price():
    return render_template('price.html')

# @application.route("/credit",methods = ['GET', 'POST'])
# def credit_account():
#     form = CreditForm()
#     return render_template('credit.html', form=form)

@application.route("/credit",methods=['GET','POST'])
def topup():
    form = CreditForm()
    if request.method == 'POST':
        pprint.pprint(request.form)

        token = request.form['id']  # Using Flask
        amount = request.form['amount']
        charge = stripe.Charge.create(
            amount= amount,
            currency='nzd',
            description='vr 360 service fee',
            source=token,
        )  # todo how to know charge is success?
        return amount
    else:
        return render_template("credit.html",form=form, key=stripe_keys['publishable_key'])

# @mobile_template('{mobile/}index.html')
def show_homepage():
    return render_template("home.html")

@application.route('/index')
@application.route("/",methods=['GET', 'POST'])
@mobilized(show_homepage)
def show_homepage():
    return render_template("home.html")
    # return redirect(url_for('show_map',place_id="ChIJJdxLbfBHDW0Rh5OtgMO10QI",lat=-36.848448,lng=174.76219100000003))

@application.route("/showmap")
# @mobile_template('{mobile/}google_map.html')
# def show_map(template):
def show_map():
    place_id = request.args.get('place_id')
    lat = request.args.get('lat')
    lng = request.args.get('lng')
    location = {
        "place_id":place_id,
        "lat":lat,
        "lng":lng
    }
    # return render_template(template,location=location)
    return render_template("google_map.html",location=location)
    # return render_template("map.html",location=location)

@application.route("/matterport/<name>")
def matterport(name):
    return render_template("3dspace.html",name=name)

@application.route("/map")
def map():
    place_id = request.args.get('place_id','ChIJJdxLbfBHDW0Rh5OtgMO10QI')
    lat = request.args.get('lat',-36.848448)
    lng = request.args.get('lng',174.76219100000003)

    location = {
        "place_id":place_id,
        "lat":lat,
        "lng":lng
    }
    return render_template("map.html",location = location)

@application.route("/virtualreality")
def virtualreality():
    return render_template("virtualreality.html")

@application.route("/ip")
def ip():
    print(str(request.__dict__))
    return jsonify(str(request.__dict__))


# @application.route("/validatetoken",methods=['POST'])
# def validatetoken():
#     access_token = request.form['access_token']
#     # print(is_token_valid(access_token))
#     if is_token_valid(access_token):
#         return "True"
#     else:
#         return "False"


@application.route("/validatetoken/<token>")
@validate_required
def validatetoken(token):
    return "True"

@application.route("/payment",methods=['GET','POST'])
def clearPayment():
    form = CreditForm()
    if request.method == 'POST':
        pprint.pprint(request.form)

        token = request.form['id']  # Using Flask
        amount = request.form['amount']
        charge = stripe.Charge.create(
            amount= amount,
            currency='nzd',
            description='vr 360 service fee',
            source=token,
        )  # todo how to know charge is success?
        return amount
    else:
        return render_template("payment.html",form=form, key=stripe_keys['publishable_key'])


if __name__ == "__main__":
    # application.run(host="192.168.20.8",debug=True)
    application.run(host="192.168.20.8",debug=True, ssl_context='adhoc')