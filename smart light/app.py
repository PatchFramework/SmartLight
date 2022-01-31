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
   #         led.on(BRIGHTNESS)
            flash("Licht ist an!")
        elif licht == "lightoff":
            session["licht"] = False
            # turn off the light 
   #         led.off()
            flash("Licht ist aus!")

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
    if session.get("zeit"):
        

        if request.method == "POST":
            session.permanent = True
            zeitloeschen = request.form.getlist("loeschen")
            #Wecker, die ausgewählt werden, werden gelöscht:
            wecker_list = licht.query.all()
            for wecker in wecker_list:
                wecker_string = f"{wecker.zeit.hour}:{wecker.zeit.minute}"
                if wecker_string in zeitloeschen:
                    wecker = datetime.strptime(wecker_string, "%H:%M").time()
                    db.session.delete(licht.query.filter(licht.zeit == wecker).first())
                    db.session.commit()
                   #übrige Wecker werden in Wecker-Entfernen-Template angezeigt und können auch noch ausgewählt werden:
            l = get_alarm_clocks()
            flash(f"Wecker was deleted: {wecker_string}")
            return render_template("weckerentfernen.html", values=l)

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
    
if __name__ == "__main__":
    # initialize the led controls

    # define the used pins for the light bulbs
    rgb_pins = (17, 22, 24) 
    pwm_frequency = 50 # in Hz
#    led = LED(*rgb_pins, pwm_frequency)    
#    led.setup()

    # start the database and webserver
    db.create_all()
    app.run(debug=True)