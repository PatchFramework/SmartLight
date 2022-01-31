from flask import Flask,render_template,request,redirect,url_for,session,flash
from datetime import timedelta, datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.mysql import TIME

# import the LED light controls
#from led import LED

# constants to controll the LED
BRIGHTNESS = 10 # out of 100
DIM_DURATION = 4 # seconds

app = Flask(__name__)
app.secret_key = "hello"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


app.permanent_session_lifetime = timedelta(days=5)
 
db = SQLAlchemy(app)

# class usersdb(db.Model):
#     _id = db.Column("id", db.Integer, primary_key=True)
#     name = db.Column("name", db.String(100))
#     email = db.Column("email", db.String(100))

#     def __init__(self, name, email):
#         self.name = name
#         self.email = email


# class lichtan(db.Model):
#     _id = db.Column("id", db.Integer, primary_key=True)
#     licht = db.Column("licht", db.String)
#     def __init__(self, licht):
#         self.licht = licht

# Database model that saves the alarm clocks
class licht(db.Model):
    ___tablename___ = 'licht'
    _id = db.Column("id", db.Integer, primary_key=True)
    # indicates if the alarm should be active or inactive
    active = db.Column("active", db.Boolean)
    # time at which the clock alarm should go off
    zeit = db.Column("zeit", db.Time)

    def __init__(self, active=True, zeit=None):
        self.licht = active
        self.zeit = zeit

# @app.route("/wecker", methods=["POST", "GET"])
# def lighton():
#     if request.method == "POST":
#         session.permanent = True
#         light = request.form["lichtschalter"]
#         session["licht"] = light
#         found_wecker = lichtan.query.filter_by(licht=licht).first()
#         if light == lighton :
#             session["licht"]=1
#         # else:
#         #     zeitpunkt = lichtan(licht)
#         #     db.session.add(zeitpunkt)
#         #     db.session.commit()


#         flash("Das Licht wurde erfolgreich eingeschalten!")
#         return redirect(url_for("weckeranzeige"))
#     else:
#         # if "zeit" in session: 
#         #     flash("Der Wecker war bereits gestellt!")
#         #     return redirect(url_for("weckeranzeige"))
#         return render_template("wecker.html")

# use this var to check whether the LED is on or off at the moment
# if light is off = False; if light is on = True
# session["licht"] = False

# redirect to the licht endpoint by default
@app.route("/", methods=["POST", "GET"])
def home():
    return redirect("/licht")

@app.route("/licht", methods=["POST", "GET"])
def lichtein():
    if request.method == "POST":
        session.permanent = True
        licht = request.form["lichtschalter"]
        
        if licht == "lighton":
            session["licht"] = True
            # turn on the light
      #      led.on(BRIGHTNESS)
            flash("Licht ist an!")
        elif licht == "lightoff":
            session["licht"] = False
            # turn off the light 
      #      led.off()
            flash("Licht ist aus!")

        # we dont need to save the data that we turn the light on immediately 
        # try:
        #     lichtein = licht.query.filter_by(licht=licht).first()
        # except:
        #     lichtein = None
        # if lichtein:
        #     session["licht"] =lichtein.licht
        # else:
        #     light = lichtan(licht)
        #     db.session.add(light)
        #     db.session.commit()


       
        return redirect(url_for("lichtein"))
    else:
        # if "licht" in session: 
        #     flash("Licht ist bereits an!")
        #     return redirect(url_for("weckerstellen"))
        return render_template("licht.html")

@app.route("/wecker", methods=["POST", "GET"])
def weckerstellen():
    if request.method == "POST":
        session.permanent = True
        #request.form["wecker"] == "weckerstellen"
        zeit = request.form.get("wecker")
        # convert zeit from format HH:MM to datetime format
        zeit = datetime.strptime(zeit, "%H:%M").time()
        print("Zeit", zeit)

        session["zeit"] = f"{zeit.hour}:{zeit.minute}"
        # found_wecker = licht.query.filter_by(zeit=zeit).first()
        found_wecker = None

        
        #session["zeit"]=zeit
        zeitpunkt = licht(active=True, zeit=zeit)
        db.session.add(zeitpunkt)
        db.session.commit()


        flash("Wecker wurde erfolgreich gestellt!")
        return redirect(url_for("weckeranzeige"))
    else:
        # if "zeit" in session: 
        #     flash("Der Wecker war bereits gestellt!")
        #     return redirect(url_for("weckeranzeige"))
        return render_template("wecker.html")

def get_alarm_clocks():
        # get all available alarms
    licht_list = licht.query.all()
    if licht_list is not None:
        # Format the alarms in hours and minutes only
        l = [f"{licht.zeit.hour}:{licht.zeit.minute}" for licht in licht_list]
        return l
    else:
        return

@app.route("/anzeige")
def weckeranzeige():
    l = get_alarm_clocks()
    return render_template("weckeranzeige.html", values=l)

@app.route("/lichtaus")
def lichtaus():
        flash(f"Licht wird ausgeschalten", "info")
        session.pop("lichtaus", None)
        return redirect(url_for("weckerstellen"))



@app.route("/loeschen", methods=["GET", "POST"])
def weckerentfernen():
#der verzweifelte Versuch, irgendwas gebacken zu bekommen
    # if request.method == "POST":
    #     session.permanent = True
    #     zeitloeschen = request.form.getlist("loeschen")
    #     session["zeit"] = zeitloeschen
    #     found_zeit = licht.query.filter_by(zeit=zeitloeschen).delete()
    #     # db.session.delete(found_zeit)
    #     db.session.commit()
    #     flash(f"Wecker was deleted: {found_zeit}")
    #     return render_template("weckerentfernen.html", values=zeitloeschen)
    # else:
    #     return render_template("weckerentfernen.html", info="Keine Wecker gefunden")

#ursprünglicher Code
    if session.get("zeit"):
        

        if request.method == "POST":
            # session.permanent = True
            # zeitloeschen = request.form.getlist("loeschen")
            # session["zeit"] = zeitloeschen
            # found_zeit = licht.query.filter_by(zeit=zeitloeschen).delete()
            # db.session.delete(found_zeit)

            zeitloeschen = request.form.getlist("loeschen")
            wecker_list = licht.query.all()
            for wecker in wecker_list:
                wecker_string = f"{wecker.zeit.hour}:{wecker.zeit.minute}"
                if wecker_string in zeitloeschen:
                    wecker = datetime.strptime(wecker_string, "%H:%M").time()
                   #db.session.delete(ItemModel.query.filter(ItemModel.time <= epoch_time).first())
                    db.session.delete(licht.query.filter(licht.zeit == wecker).first())
                    #delete(licht.zeit)
                    db.session.commit()
            # found_zeit = licht.query.filter_by(zeit=zeitloeschen).delete()
            # db.session.delete(zeitloeschen)
            # db.session.commit()
            flash(f"Wecker was deleted: {wecker_string}")
            return render_template("weckerentfernen.html")

        else:
            if "zeit" in session:
                zeit = session["zeit"]
                l = get_alarm_clocks()
                return render_template("weckerentfernen.html", values=l)
    
    else:
        flash("Es sind keine Wecker gestellt!")
        return redirect(url_for("weckerstellen"))
@app.route("/test")
def test():
    return render_template("new.html", content="Testing")
    
  #  , methods=["POST", "GET"])
# def user():
#     email = None
#     if "user" in session:
#         user = session["user"]

#         if request.method == "POST":
#             email = request.form["email"]
#             session["email"] = email
#             found_user = usersdb.query.filter_by(name=user).first()
#             found_user.email = email
#             db.session.commit()
#             flash(f"Email was saved: {email}")
#         else:
#             if "email" in session:
#                 email = session["email"]

#         return render_template("user.html", email=email)
#     else:
#         flash("You are not logged in!")
#         return redirect(url_for("login"))
# @app.route("/")
# def home():
#     return render_template("index.html")

# @app.route("/view")
# def view():
#     return render_template("view.html", values=usersdb.query.all())

# @app.route("/login", methods=["POST", "GET"])
# def login():
#     if request.method == "POST":
#         session.permanent = True
#         user = request.form["nm"]
#         session["user"] = user
#         found_user = usersdb.query.filter_by(name=user).first()
#         if found_user:
#             session["email"] =found_user.email
#         else:
#             usr = usersdb(user, "")
#             db.session.add(usr)
#             db.session.commit()


#         flash("Login Successful!")
#         return redirect(url_for("user"))
#     else:
#         if "user" in session: 
#             flash("Already Logged In!")
#             return redirect(url_for("user"))
#         return render_template("login.html")

# @app.route("/user", methods=["POST", "GET"])
# def user():
#     email = None
#     if "user" in session:
#         user = session["user"]

#         if request.method == "POST":
#             email = request.form["email"]
#             session["email"] = email
#             found_user = usersdb.query.filter_by(name=user).first()
#             found_user.email = email
#             db.session.commit()
#             flash(f"Email was saved: {email}")
#         else:
#             if "email" in session:
#                 email = session["email"]

#         return render_template("user.html", email=email)
#     else:
#         flash("You are not logged in!")
#         return redirect(url_for("login"))
# @app.route("/test")
# def test():
#     return render_template("new.html", content="Testing")

# @app.route("/logout")
# def logout():
#         flash(f"You have been logged out!", "info")
#         session.pop("user", None)
#         session.pop("email", None)
#         return redirect(url_for("login"))



if __name__ == "__main__":
    # initialize the led controls

    # define the used pins for the light bulbs
    rgb_pins = (17, 22, 24) 
    pwm_frequency = 50 # in Hz
   # led = LED(*rgb_pins, pwm_frequency)    
  #  led.setup()

    # start the database and webserver
    db.create_all()
    app.run(debug=True)