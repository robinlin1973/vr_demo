# coding: utf-8

from flask import Flask, render_template,url_for,redirect,request,make_response
import boto3
from datetime import timedelta
from functools import update_wrapper
from flask_mobility import Mobility
from flask_mobility.decorators import mobile_template,mobilized

application = Flask(__name__, template_folder="templates")
Mobility(application)
s3 = boto3.resource('s3')
s3_bucket_name = 'vr-content'
vr_s3_folder = 'https://s3.us-east-2.amazonaws.com/vr-content/'
bucket = s3.Bucket(s3_bucket_name)

@application.route("/fetch_vr/<string:place_id>")
def fetch_vr(place_id):
    # # key = place_id + '.jpg'
    # key = place_id+'/index.htm'
    # objs = list(bucket.objects.filter(Prefix=key))
    # if len(objs) > 0 and objs[0].key == key:
    #     file_url = vr_s3_folder + key
    #     # print("Exists! {}".format(file_url))
    #     # return render_template("panolens.html", address=file_url)
    #     # return redirect("https://www.3dvista.com/samples/real_estate_virtual_tour.html", code=302)
    #     return redirect("https://s3.us-east-2.amazonaws.com/vr-content/"+key, code=302)
    # else:
    #     # print("Doesn't exist, show upload html")
    #     return render_template("upload.html",place_id=place_id)
    # return render_template("matterport_demo.html")
    return render_template("3dspace.html",name="JGPnGQ6hosj")

@application.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

@application.route("/vrservice")
def vr_service():
    return render_template("vrservice.html")

# @mobile_template('{mobile/}index.html')
def show_homepage():
    return render_template("index.html")

@application.route("/",methods=['GET', 'POST'])
@mobilized(show_homepage)
def show_homepage():
    return redirect(url_for('show_map',place_id="ChIJJdxLbfBHDW0Rh5OtgMO10QI",lat=-36.848448,lng=174.76219100000003))

@application.route("/showmap")
@mobile_template('{mobile/}google_map.html')
def show_map(template):
    place_id = request.args.get('place_id')
    lat = request.args.get('lat')
    lng = request.args.get('lng')
    location = {
        "place_id":place_id,
        "lat":lat,
        "lng":lng
    }
    return render_template(template,location=location)

@application.route("/matterport/<name>")
def matterport(name):

    return render_template("3dspace.html",name=name)


@application.route("/panotour",methods=['GET', 'POST'])
def panotour():
    return render_template("panotour.html")

@application.route("/d3vista",methods=['GET', 'POST'])
def d3vista():
    return redirect("https://www.3dvista.com/samples/real_estate_virtual_tour.html", code=302)

if __name__ == "__main__":
    application.run(host="192.168.20.8",debug=True)