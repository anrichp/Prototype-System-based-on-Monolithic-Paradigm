from flask import Flask,render_template, url_for, session, request, redirect, flash, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from functools import wraps


app = Flask(__name__) #creates a flask app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db' #configure users database
app.config['SECRET_KEY']='thisissupposedtobemysecret' #configure a secret key

db = SQLAlchemy(app)# creates a database
bcrypt=Bcrypt(app)# instatiate the bcrypt to help in hashing of passwords
db2 = SQLAlchemy(app)


from my_app.forms import Login, Registration #importing forms
from my_app.models import Astronaut, Admin #importing models
blueprint=Blueprint("blueprint", __name__, static_folder="static", template_folder="templates") # creating a blueprint


from my_app.models import Admin

#decorator function to check if user baccessing certain paths are authenticated, if not they are taken back to login
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if "username" in session:
            return f(*args, **kwargs)
        else:
            flash("You need to login first!")
            return redirect(url_for("astronautlogin"))
    return wrap

#decorator function to check if administrative user accessing certain paths are authenticated, if not they are taken back to login
def adminlogin_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if "adminusername" in session:
            return f(*args, **kwargs)
        else:
            flash("You need to login first!")
            return redirect(url_for("blueprint.adminlogin"))
    return wrap

@blueprint.route("/", methods=["POST", "GET"])
def adminlogin():
    if "adminusername" in session:
        return redirect(url_for('blueprint.admindashboard'))# this is for persistence purposes, if the user is logged in they should stay logged in.
    form=Login(request.form) # create an instace of the login form
    if request.method == 'POST' and form.validate(): #if the method is post and the form validates
        admin=Admin.query.filter_by(username=form.username.data).first()#find the astronaut in the database
        if admin and bcrypt.check_password_hash(admin.password, form.password.data): #if the astronaut exists and the password hash matches the hash fro entered password
            session['adminusername']=form.username.data #add the user to session
            flash(f'Welcome {form.username.data}. You are now logged in.', 'success')
            return redirect(request.args.get('next') or url_for('blueprint.admindashboard'))
        else:
            flash(f'Wrong password/email. Please try again.', 'danger')
    return render_template("admin/login.html", form=form, title="Login page")

#this path should only be acccessible to logged in administartors so we use the decorator.
@blueprint.route("/dashboard")
@adminlogin_required #applying the adminlogin decorator
def admindashboard():
    return "<h1>Welcome to admin dashboard</h1>"

#this is for admin registration
@blueprint.route("/register", methods=["POST", "GET"])
def register():
    form=Registration(request.form) #create an instace of the registration form
    if request.method == 'POST' and form.validate(): # if the reuest method is post 
        hashedpass=bcrypt.generate_password_hash(form.password.data)#encrypt the password
        admin = Admin(name=form.name.data, username=form.username.data, email=form.email.data, password=hashedpass)
        db.session.add(admin) #add data to the db
        db.session.commit() #commit the process for the actual save.
        flash(f'Welcome {form.username.data}. Thank you for registering.', 'success')
        return redirect(url_for("blueprint.adminlogin"))
    return render_template("admin/register.html", form=form)

#this is for admin logout
@blueprint.route("/logout")
@login_required #applying the login decorator.
def logout():
    session.clear()
    flash("You have successfully logged out.")
    return redirect(url_for("blueprint.adminlogin"))

app.register_blueprint(blueprint, url_prefix="/admin") #registering the blueprint to our app


#astromaut login page
@app.route("/", methods=["POST", "GET"])
def astronautlogin():
    if "username" in session:
        return redirect(url_for('dashboard')) #for persistence purposes
    form=Login(request.form) # create an instace of the login form
    if request.method == 'POST' and form.validate(): #if the method is post and the form validates
        astronaut=Astronaut.query.filter_by(username=form.username.data).first()#find the astronaut in the database
        if astronaut and bcrypt.check_password_hash(astronaut.password, form.password.data): #if the astronaut exists and the password hash matches the hash fro entered password
            session['username']=form.username.data #add the user to session
            flash(f'Welcome {form.username.data}. You are now logged in.', 'success')
            return redirect(request.args.get('next') or url_for('dashboard'))
        else:
            flash(f'Wrong password/email. Please try again.', 'danger')
    return render_template("astronaut/login.html", form=form, title="Login page")

#this route also should only be accessible to logged in astronaut
@app.route('/dashboard')
@login_required #applying the login decorator.
def dashboard():
    return "<h1>Welcome to dashboard</h1>"

@app.route("/register", methods=["POST", "GET"])
def register():
    form=Registration(request.form) #create an instace of the Registration form
    if request.method == 'POST' and form.validate(): # if the request method is post 
        hashedpass=bcrypt.generate_password_hash(form.password.data)#encrypt the password
        astronaut = Astronaut(name=form.name.data, username=form.username.data, email=form.email.data, password=hashedpass)
        db.session.add(astronaut) #add to db
        db.session.commit() #commit the process for the actual save.
        flash(f'Welcome {form.username.data}. Thank you for registering.', 'success')
        return redirect(url_for("astronautlogin"))
    return render_template("astronaut/register.html", form=form)

#astronaut logout route
@app.route("/logout")
@login_required #applying the login decorator.
def logout():
    session.clear() #clear the session values
    flash("You have successfully logged out.")
    return redirect(url_for("astronautlogin")) #then redirecting to login