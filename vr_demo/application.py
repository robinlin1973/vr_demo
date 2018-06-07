# coding: utf-8

from flask import Flask, render_template

application = Flask(__name__, template_folder="templates")

#demo_vr_url = "<a href='http://m.detu.com/zh/pano/show/434339?from=singlemessage'>Loading VR</a>"
demo_vr_url = "http://m.detu.com/zh/pano/show/434339?from=singlemessage"

@application.route('/')
def fullmap():
    return render_template('google_search.html')

@application.route("/fetch_vr/<string:address>")
def fetch_vr(address):
    return "NA"#demo_vr_url#get_vr_url(para)

@application.route("/upload")
def upload_vr():
    print("show upload form")
    return render_template("upload.html")

if __name__ == "__main__":
    application.run(debug=True, use_reloader=True)
