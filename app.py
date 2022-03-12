from flask import Flask, render_template, redirect, session, flash, request, abort
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User, Business
from forms import SignUpForm, LoginForm, EditUserForm
import requests, os, json
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)


uri = os.environ.get('DATABASE_URL', 'postgresql:///first_capstone_db')
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)

secret = os.environ["SECRET_KEY"]
headers = dict(json.loads(os.environ["HEADERS"]))
google_map_key = os.environ["GOOGLE_MAP_KEY"]



app.config['SQLALCHEMY_DATABASE_URI'] = uri
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = os.environ.get('SECRET_KEY', secret)
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False


connect_db(app)

toolbar = DebugToolbarExtension(app)

@app.route("/")
def homePage():
    """Show homepage with links to site areas."""
    if "user_id" not in session:
        return redirect("/half-homepage")
    
    return render_template("full_homepage.html")

   
@app.route("/full-homepage")
def fullHomePage():
    """Show complete homepage to the user"""
    if "user_id" not in session:
        return redirect("/half-homepage")


    return render_template("full_homepage.html")


@app.route("/half-homepage")
def halfHomePage():
    """Home page. When User is not logged in"""

    return render_template("index.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    """Registers a user. Produce form and handles form submissions."""

    form = SignUpForm()

    if form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        password = form.password.data

        new_user = User.register(first_name, last_name, email, password)

        db.session.add(new_user)

        db.session.commit()

        session['user_id'] = new_user.id

        session['first_name'] = new_user.first_name

        flash("Welcome! You successfully created your account!")

        return redirect("/full-homepage")
    else:
        return render_template("users/signup.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Login a user"""

    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = User.authenticate(email, password)

        if user:
            flash(f"Welcome Back, {user.first_name}!")
            session['user_id'] = user.id
            session['first_name'] = user.first_name

            return redirect("/full-homepage")
        else:
            form.email.errors = ['Invalid email/password.']

    return render_template("users/login.html", form=form)


@app.route("/logout")
def logout_user():
    flash(f"Goodbye!")
    session.pop('user_id')
    return redirect("/")


@app.route("/users/edit", methods=["GET", "POST"])
def process_user_edit():
    """Process user edit form."""

    user_id = session["user_id"]

    user = User.query.get_or_404(user_id)
    form = EditUserForm(obj=user)

    if form.validate_on_submit():
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data 
        session['first_name'] = user.first_name
        db.session.add(user)
        db.session.commit()

        return redirect("/")
    else:
        return render_template("/users/edit.html", form=form)


@app.route("/users/search")
def searchYelp():
    """Search Yelp API."""

    
    term = request.args["restaurant"]
    location = request.args["location"]

    if term == "" or location == "":
        abort(500)

    res = requests.get("https://api.yelp.com/v3/businesses/search",
                    params={"term": term, "location": location},
                    headers=headers)
    try:
        result = res.json()["businesses"]
        return render_template("full_homepage.html", result=result, term=term, location=location) 
    except KeyError:
        abort(500)

        
@app.route("/business/<business_id>")
def biz_info(business_id):
    """Show more information about a business."""

    res = requests.get(f"https://api.yelp.com/v3/businesses/{business_id}", headers=headers)

    result = res.json()
    if result:
        data = {"lat": result["coordinates"]["latitude"], "lng": result["coordinates"]["longitude"], "end": result["location"]["display_address"][0]}
    return render_template("business_info.html", result=result, data=data, google_map_key=google_map_key)


@app.route("/business/favorite/<business_id>")
def add_favorite(business_id):
    """Add business to favorite"""

    user_id = session["user_id"]

    user = User.query.get_or_404(user_id)

    try:
        business = Business(business_yelp_id=business_id)

        business.users.append(user)
    
        db.session.add(business)

        db.session.commit()

        flash("Added to your favorites!")

        return redirect(f"/add/favorites/{business_id}")
    except:
        return redirect(f"/add/favorites/{business_id}")



@app.route("/add/favorites/<business_id>")
def show_added_favorite(business_id):

    favorite = Business.query.filter_by(business_yelp_id=business_id).first()
    fav_id = favorite.business_yelp_id
    res = requests.get(f"https://api.yelp.com/v3/businesses/{fav_id}", headers=headers)
    result = res.json()
    data = {"name": result["name"], "image": result["image_url"], "address": result["location"]["display_address"][0]}
    return render_template("see_favorites.html", data=data)


@app.route("/favorites")
def show_favorite():
    """Show Users favorites"""

    tuple_of_yelp_ids = db.session.query(Business.business_yelp_id).all()

    list_of_yelp_id = []

    for single_yelp_id in tuple_of_yelp_ids:
        res = requests.get(f"https://api.yelp.com/v3/businesses/{single_yelp_id[0]}", headers=headers)
        result = res.json()
        list_of_yelp_id.append(result)
    return render_template("view_favorite.html", main_fav=list_of_yelp_id)
    

@app.route("/favorites/<business_id>/delete")
def delete_favorite(business_id):
    """Delete User favorite"""

    Business.query.filter_by(business_yelp_id=business_id).delete()

    db.session.commit()
    
    return redirect("/favorites")


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404


@app.errorhandler(500)
def server_error(e):
    # note that we set the 500 status explicitly
    return render_template('500.html'), 500


@app.errorhandler(requests.exceptions.ConnectionError)
def handle_bad_request(e):
    return render_template('connection.html')
