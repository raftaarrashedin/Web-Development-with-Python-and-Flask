#---------------------------------------------------------------------------------
# importing the dependencies
from flask import Flask, render_template,request
from flask_sqlalchemy import SQLAlchemy
# from flask_mail import Mail
import json
from datetime import datetime


#---------------------------------------------------------------------------------
# configuring the json file
local_server = True
with open('config.json','r') as c :
    params = json.load(c) ['params']

#---------------------------------------------------------------------------------
# flask app calling
app = Flask(__name__)

#---------------------------------------------------------------------------------
# mail setting up
# app.config.update(

#         MAIL_SERVER = 'smtp.gmail.com',
#         MAIL_PORT = '465',
#         MAIL_USE_SSL = True,
#         MAIL_USERNAME = params['gmailuser'],
#         MAIL_PASSWORD = params['gmailpassword']
#     )

# mail = Mail(app)

#---------------------------------------------------------------------------------
# configuring the database
if (local_server) :
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
else :
    app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri']

db = SQLAlchemy(app)

#---------------------------------------------------------------------------------
# connecting to the contact table from flask_and_python database
class Contact(db.Model):

    serial_no = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    message = db.Column(db.String(255), nullable=False)


#---------------------------------------------------------------------------------
# connecting to the post table from flask_and_python database
class Posts(db.Model) :

    serial_no = db.Column(db.Integer, primary_key=True) 
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(50), nullable=False)
    slug = db.Column(db.String(50), nullable=False)
    image_file = db.Column(db.String(250), nullable=False)


#---------------------------------------------------------------------------------
# main page routing
@app.route("/")

def hello() :
	return render_template('index.html',params=params)



#---------------------------------------------------------------------------------
# dashboard page routing
@app.route("/dashboard", methods=['GET','POST'])
def dashboard() :

    if request.method == 'POST' : 

        pass
        # redirect to admin panel
    else :
        return render_template('login.html',params=params)



#---------------------------------------------------------------------------------
# post page routing
@app.route("/posts/<string:post_slug>", methods=['GET']) 
def post_route(post_slug) :

    post = Posts.query.filter_by(slug = post_slug).first()

    return render_template('posts.html', params=params, post=post)

#---------------------------------------------------------------------------------
# about page routing 
@app.route("/about")

def raftaar() :
	name = "Rashedin"
	return render_template('about.html',params = params)

#---------------------------------------------------------------------------------
# useless main_page routing
@app.route("/main_page")

def main_page() :
	return render_template('main_page.html',params = params)

#---------------------------------------------------------------------------------
# portfolio_page routing
@app.route("/portfolio") 

def portfolio() :
	return render_template('portfolio.html',params = params)

#---------------------------------------------------------------------------------
# inner page routing
@app.route('/inner-page') 
def inner_page() :
	return render_template('inner-page.html',params = params)


#---------------------------------------------------------------------------------
# portfolio-details page routing
@app.route('/portfolio-details') 
def portfolio_details() :
	return render_template('portfolio-details.html',params = params)


#---------------------------------------------------------------------------------
# inserting value into database
@app.route("/contact", methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Fetch data and add it to the database
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')  # Updated the form field name
        message = request.form.get('message')

        # Creating a new Contacts instance
        new_contact = Contact(name=name, email=email, subject=subject, message=message)

        try:
            # Adding and committing the new contact to the database
            db.session.add(new_contact)
            db.session.commit()
            # mail.send_message('New message from' + name,
            #     sender = email,
            #     recipient = [params['gmail-user']],
            #     body = message
            #     )
            return "Contact form submitted successfully!"
        except Exception as e:
            # Rolling back in case of an error
            db.session.rollback()
            return f"Error: {str(e)}"

    return render_template('contact.html',params = params)

# running app
app.run(debug = True)