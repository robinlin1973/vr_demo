# coding: utf-8

from flask import Flask, render_template,url_for,redirect,request,make_response,flash,jsonify
import boto3
from flask_mobility import Mobility
from flask_mobility.decorators import mobile_template,mobilized
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, SubmitField, RadioField,SelectField
from wtforms import validators, ValidationError
from flask_mail import Mail,  Message
import json

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


mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": 'abinlaa@gmail.com',
    "MAIL_PASSWORD": 'Sp-3308897'
}

application.config.update(mail_settings)
mail = Mail(application)

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


# @application.route("/quotation", methods = ['GET', 'POST'])
# def quotation():
#     form = ContactForm()
#     if request.method == 'POST':
#         if form.validate() == False:
#             flash('All fields are required.')
#             return render_template('quotation.html', form=form)
#         else:
#             with application.app_context():
#                 msg = Message(subject="Quotation Received"+form.data['address'],
#                               sender=application.config.get("MAIL_USERNAME"),
#                               recipients=[form.data['email']],  # replace with your email for testing
#                               body=json.dumps(form.data))
#                 mail.send(msg)
#             flash('Quote request received, We will contact you shortly!')
#             return redirect("/", code=302)
#     elif request.method == 'GET':
#         return render_template('quotation.html', form=form)

# @mobile_template('{mobile/}index.html')
def show_homepage():
    return render_template("home.html")

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

#
# @application.route("/panotour",methods=['GET', 'POST'])
# def panotour():
#     return render_template("panotour.html")

# @application.route("/d3vista",methods=['GET', 'POST'])
# def d3vista():
#     return redirect("https://www.3dvista.com/samples/real_estate_virtual_tour.html", code=302)

# @application.route("/faq")
# def faq():
#     return render_template("faq.html")
#
# @application.route("/about")
# def about():
#     return render_template("about.html")

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


@application.route("/signup",methods=['POST'])
def signup():
    print("received signup info")
    return redirect(request.referrer)

# @application.route("/test")
# def test():
#     return render_template("sign.html")


if __name__ == "__main__":
    # application.run(host="192.168.20.8",debug=True)
    application.run(host="192.168.20.8",debug=True, ssl_context='adhoc')