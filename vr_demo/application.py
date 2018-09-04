# coding: utf-8
from functools import wraps
from flask import Flask, render_template,url_for,redirect,request,flash,session,jsonify,make_response
from flask_mail import Mail,Message
import json
import stripe
import os
import pprint
from support import ContactForm,CreditForm,SigninForm, SignupForm,User
from flask_bootstrap import Bootstrap
from warrant import Cognito
import cognitojwt
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from datetime import datetime

# use the stripe keys to handle the payment
stripe_keys = {
  'secret_key': os.getenv('SECRET_KEY'),
  'publishable_key': os.getenv('PUBLISHABLE_KEY')
}
pem = os.getenv('PEM')    #todo add to production envrionment path
stripe.api_key = stripe_keys['secret_key']
application = Flask(__name__, template_folder="templates")
login_manager = LoginManager()
login_manager.init_app(application)
login_manager.login_view = 'sign'
application.secret_key = os.getenv('APP_SECRET_KEY') #todo add to production envrionment path

cognito_userpool_id = os.getenv('COGNITO_USERPOOL_ID')#todo add to production envrionment path
cognito_userpool_region = os.getenv('COGNITO_USERPOOL_REGION')#todo add to production envrionment path
cognito_client_id = os.getenv('COGNITO_CLIENT_ID') #todo add to production envrionment path



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
bootstrap = Bootstrap(application)


@login_manager.user_loader
def user_loader(session_token):
    """Populate user object, check expiry"""
    if "expires" not in session:
        return None

    expires = datetime.utcfromtimestamp(session['expires'])
    expires_seconds = (expires - datetime.utcnow()).total_seconds()
    if expires_seconds < 0:
        return None

    user = User()
    user.id = session_token
    if 'credit' in session:
         user.credit = session['credit']
    else:
        user.credit = '0'

    return user

# route to show index/home page
@application.route('/index')
@application.route("/", methods=['GET', 'POST'])
def index():
    return render_template("index.html")

@application.route("/virtualreality")
def show_vr():
    return render_template("virtualreality.html")

@application.route("/price")
@login_required
def price():
    return render_template('price.html')

@application.route("/contact", methods = ['GET', 'POST'])
def show_contact():
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

# def flash_errors(form,formname):
#     """Flashes form errors"""
#     for field, errors in form.errors.items():
#         for error in errors:
#             flash(u"%s %s - %s" % (formname, getattr(form, field).label.text,error), 'error')
#             print(u"%s %s - %s" % (formname, getattr(form, field).label.text,error), 'error')

def redirect_url(default='index'):
    return request.args.get('next') or \
           request.referrer or \
           url_for(default)

@application.route("/sign",methods = ['GET','POST'])
def sign():
    signinform = SigninForm(prefix="signin")
    signupform = SignupForm(prefix="signup")

    if request.method == 'POST':
        form = request.form
        pprint.pprint(form)
        if request.form['btn'] == 'Signin':
            # session["active_panel"] = "login-form-link"
            if signinform.validate_on_submit():
                try:
                    auth_cognito = Cognito(cognito_userpool_id, cognito_client_id,
                                           user_pool_region=cognito_userpool_region,
                                           username=form['signin-username'])
                    auth_cognito.authenticate(password=form['signin-password'])
                    decoded_token = cognitojwt.decode(auth_cognito.id_token,cognito_userpool_region,cognito_userpool_id,cognito_client_id)
                    user = auth_cognito.get_user()
                    credit = user._data['custom:credit']
                # except NotAuthorizedException as e:
                #     flash(e.response['Error']['Message'])
                #     return redirect(request.referrer)
                except Exception as e:
                    if hasattr(e, 'message'):
                        msg = e.message
                    else:
                        msg = str(e)
                    flash(msg, 'error')
                    return redirect(request.referrer)
                else:
                    flash("Signin Successfully!")

                    user = User()
                    user.id = decoded_token["cognito:username"]
                    user.credit = credit
                    session['credit'] = credit
                    session['expires'] = decoded_token["exp"]
                    session['refresh_token'] = auth_cognito.refresh_token
                    session['id_token'] = auth_cognito.id_token
                    session['access_token'] = auth_cognito.access_token
                    login_user(user, remember=True)
                    next_url = request.args.get('next','index').strip("/")
                    print("next_url:{}".format(next_url))
                    return redirect(url_for(next_url))

            else:
                flash(signinform.errors)
                return redirect(request.referrer)

        elif request.form['btn'] == 'Signup':
            # session["active_panel"] = "register-form-link"
            if signupform.validate_on_submit():
                try:
                    u = Cognito(cognito_userpool_id, cognito_client_id,cognito_userpool_region)
                    u.add_base_attributes(email=form['signup-email'])
                    u.add_custom_attributes(credit='0')
                    u.register(form['signup-username'], form['signup-password'])
                except Exception as e:
                    if hasattr(e, 'message'):
                        msg = e.message
                    else:
                        msg = str(e)
                    flash(msg, 'error')
                else:
                    pprint.pprint(session)
                    flash ("Finish the signup by confirm link in mailbox")
            else:
                flash(signupform.errors,"error")

            return redirect(request.referrer)

    return render_template('sign.html', signinform=signinform,signupform=signupform)

@application.route("/signout")
@login_required
def signout():
    if 'id_token' in session and 'access_token' in session and 'refresh_token':
        u = Cognito(cognito_userpool_id, cognito_client_id,cognito_userpool_region,id_token=session['id_token'],
                    refresh_token=session['refresh_token'],access_token=session['access_token'])
        u.logout()

    logout_user()
    # to do
    return redirect(url_for('index'))

@application.route("/topup",methods=['GET','POST'])
@login_required
def topup():
    form = CreditForm()
    if request.method == 'POST':
        msg = ""

        token = request.form['id']  # Using Flask
        amount = request.form['amount']
        charge = stripe.Charge.create(
            amount= amount,
            currency='nzd',
            description='vr 360 service fee',
            source=token,
        )  # todo how to know charge is success?
        try:
            if 'id_token' in session and 'access_token' in session and 'refresh_token':
                u = Cognito(cognito_userpool_id, cognito_client_id, cognito_userpool_region, id_token=session['id_token'],
                            refresh_token=session['refresh_token'], access_token=session['access_token'],
                            username=current_user.id)
                topup_amount = int(float(amount)/100)
                user = u.get_user()
                balance = int(user._data['custom:credit'])
                new_balance = topup_amount + balance
                u.update_profile({'custom:credit': str(new_balance)})
                user = u.get_user()
                balance = user._data['custom:credit']
                session['credit'] = balance
                current_user.credit = balance
            else:
                raise Exception("Charged,but fail to topup the account")
        except Exception as e:
            if hasattr(e, 'message'):
                msg = e.message
            else:
                msg = e
        else:
            msg = "Topup Successfully"
        finally:
            # flash(msg)
            return msg#render_template("topup.html",form=form, key=stripe_keys['publishable_key'])#redirect(url_for("topup"))

    elif request.method == 'GET':
        return render_template("topup.html",form=form, key=stripe_keys['publishable_key'])

if __name__ == "__main__":
    # application.run(host="192.168.20.8",debug=True)
    application.run(host="192.168.20.8",debug=True,ssl_context='adhoc')