# coding: utf-8

from flask import Flask, render_template,url_for,redirect,request
import boto3
# from bs4 import BeautifulSoup
# import requests

application = Flask(__name__, template_folder="templates")

#demo_vr_url = "<a href='http://m.detu.com/zh/pano/show/434339?from=singlemessage'>Loading VR</a>"
# demo_vr_url = "http://showroom.littleworkshop.fr/"#"http://m.detu.com/zh/pano/show/434339?from=singlemessage"
# sample_place_id = "ChIJ2YzT-RRLDW0RGqHdX0k4wJM"
s3 = boto3.resource('s3')
s3_bucket_name = 'vr-content'
vr_s3_folder = 'https://s3.us-east-2.amazonaws.com/vr-content/'
bucket = s3.Bucket(s3_bucket_name)

@application.route("/fetch_vr/<string:place_id>")
def fetch_vr(place_id):
    key = place_id + '.jpg'
    objs = list(bucket.objects.filter(Prefix=key))
    if len(objs) > 0 and objs[0].key == key:
        file_url = vr_s3_folder + key
        print("Exists! {}".format(file_url))
        return render_template("panolens.html", address=file_url)
    else:
        # print("Doesn't exist, show upload html")
        return render_template("upload.html",place_id=place_id)


# @application.route("/upload")
# def upload_vr():
#     # print("show upload form")
#     return render_template("upload.html")

@application.route("/",methods=['GET', 'POST'])
def show_homepage():
    return render_template("index.html")

@application.route("/showmap")
def show_map():
    place_id = request.args.get('place_id')
    lat = request.args.get('lat')
    lng = request.args.get('lng')
    location = {
        "place_id":place_id,
        "lat":lat,
        "lng":lng
    }
    return render_template("google_map.html",location=location)


if __name__ == "__main__":
    #application.run(debug=True, use_reloader=True)
    application.run()#host="192.168.20.8"