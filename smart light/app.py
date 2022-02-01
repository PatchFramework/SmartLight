from flask import Flask,render_template,request,redirect,url_for,session,flash
from datetime import timedelta, datetime, date

# database related imports
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, Column, Boolean, Integer, Time
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.dialects.mysql import TIME

from time import sleep
import threading

# import the LED light controls
from led import LED

# constants to controll the LED
# maximal brightness of the alarm
BRIGHTNESS = 10 # out of 100
# slowly dim the light on over this duration
DIM_DURATION = 4 # seconds
# check the database for alarms every x seconds
CHECK_DB_INTERVALL = 60 # seconds
# if the light alarm goes off, keep the light on for this duration
STAY_ON_DURATION = 10 # seconds
# dim the light to BRIGHTNESS over the duration of x seconds
DIM_ON_DURATION = 10 # seconds
# dim the light off over the duration of x seconds
DIM_OFF_DURATION = 3 # seconds


#############################
##### webserver config ######
#############################

app = Flask(__name__)
app.secret_key = "hello"
app.permanent_session_lifetime = timedelta(days=5)

#############################
###### Database config ######
#############################

# create a db session that can be called from multiple threads
engine = create_engine('sqlite:///wecker.db', echo=True)
db = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()
Base.query = db.query_property()

# Database model that is used to save and read the alarm clocks
class licht(Base):
    __tablename__ = 'licht'
    _id = Column("id", Integer, primary_key=True)
    # indicates if the alarm should be active or inactive
    active = Column("active", Boolean)
    # time at which the clock alarm should go off
    zeit = Column("zeit", Time)

    def __init__(self, active=True, zeit=None):
        self.licht = active
        self.zeit = zeit

# gracefully shutdown the database on webserver shutdown
@app.teardown_appcontext
def shutdown_session(exception=None):
    db.remove()


#############################
##### webserver routes ######
#############################

# redirect to the licht endpoint by default
@app.route("/", methods=["POST", "GET"])
def home():
    return redirect("/licht")

@app.route("/licht", methods=["POST", "GET"])
def lichtein():
    licht_status=session.get("licht")
    if licht_status == True:
        flash("Licht ist gerade an")
    else: 
        flash("Licht ist gerade aus")
    if request.method == "POST":
        session.permanent = True
     
        licht = request.form["lichtschalter"]
        if licht ==[]:
            flash("Bitte eine Auswahl treffen!")
        if licht == "lighton":
            session["licht"] = True
            # turn on the light
            led.on(BRIGHTNESS)
            flash("Licht ist an!")
            return render_template("licht.html")
        elif licht == "lightoff":
            session["licht"] = False
            # turn off the light 
            led.off()
            flash("Licht ist aus!")      
            return render_template("licht.html")

     #   return redirect(url_for("lichtein"))
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
        if zeit == '':
            flash("Es wurde keine Zeit eingestellt. Bitte erneut versuchen.")
            return redirect(url_for("weckerstellen"))
        zeit = datetime.strptime(zeit, "%H:%M").time()
        print("Zeit", zeit)

        session["zeit"] = f"{zeit.hour}:{zeit.minute}"
        # found_wecker = licht.query.filter_by(zeit=zeit).first()
        found_wecker = None

        
        #session["zeit"]=zeit
        zeitpunkt = licht(active=True, zeit=zeit)
        # keep in mind that db is the session with the db
        db.add(zeitpunkt)
        db.commit()


        flash("Wecker wurde erfolgreich gestellt!")
        return redirect(url_for("weckeranzeige"))
    else:
        # if "zeit" in session: 
        #     flash("Der Wecker war bereits gestellt!")
        #     return redirect(url_for("weckeranzeige"))
        return render_template("wecker.html")

def get_alarm_clocks(str_format=True, threadsave_db_session=db):
    # get all available alarms
    licht_list = threadsave_db_session.query(licht).all()
    if licht_list is not None:
        if str_format:
            # Format the alarms in hours and minutes only
            l = [f"{licht.zeit.hour}:{licht.zeit.minute}" for licht in licht_list]
        else:
            # datetime.time() object; not formatted as a string 
            l = [licht.zeit for licht in licht_list]
        return l
    else:
        return

@app.route("/anzeige")
def weckeranzeige():
    l = get_alarm_clocks()
    if l == []:
        flash("Es sind keine Wecker gestellt.")
        # return redirect(url_for("weckerstellen"))
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
            if wecker_list==[]:
                flash("Keine Wecker vorhanden! Es können keine Wecker gelöscht werden. ")
                return redirect(url_for("weckerentfernen"))            
            for wecker in wecker_list:
                wecker_string = f"{wecker.zeit.hour}:{wecker.zeit.minute}"
                if wecker_string in zeitloeschen:
                    wecker = datetime.strptime(wecker_string, "%H:%M").time()
                    db.delete(licht.query.filter(licht.zeit == wecker).first())
                    db.commit()
                    flash(f"Wecker wurde gelöscht: {wecker_string}")
                   #übrige Wecker werden in Wecker-Entfernen-Template angezeigt und können auch noch ausgewählt werden:
            l = get_alarm_clocks()
            
            return render_template("weckerentfernen.html", values=l)

        else:
            if "zeit" in session:
                zeit = session["zeit"]
                l = get_alarm_clocks()
                return render_template("weckerentfernen.html", values=l)
    
    else:
        flash("Es sind keine Wecker gestellt!")
        return redirect(url_for("weckerstellen"))

#############################
##### Utility functions #####
#############################

def equal_time_obj(t1, t2):
    """
    Takes two datetime.time objects and returns true if they are 
    identical in HH:mm format. seconds and microseconds are ignored.
    """
    # truncate time to hour and minutes only; remove seconds and microseconds
    t1_trunc = t1.replace(second=0, microsecond=0)
    t2_trunc = t2.replace(second=0, microsecond=0) 
    return t1_trunc == t2_trunc

# asynchronous background thread that checks if alarms are due 
def check_alarm_every_dt(dt=CHECK_DB_INTERVALL):
    while True:
        # try to receive the current alarm clocks
        # get all alarm clocks as datetime.time() objects
        alarms = get_alarm_clocks(str_format=False, threadsave_db_session=db)
        print("Checking alarms in the database:", alarms)

        if alarms is not None:
            current_time = datetime.now().time()
            for time in alarms:
                # ring if the alarm is equal to the current time in HH:mm format
                ring = equal_time_obj(current_time, time)
                
                # if one of the alarms is due
                if ring:
                    print("Ringing alarm", time, "at", current_time)
                    led.dim_on(BRIGHTNESS, DIM_ON_DURATION)
                    sleep(STAY_ON_DURATION)
                    led.dim_off(DIM_OFF_DURATION)
        # wait one time intervall
        sleep(dt)

#############################
####### Main function #######
#############################

if __name__ == "__main__":
    # start the backgound thread that activates the light if an alarm should go off
    b = threading.Thread(name="background", target=check_alarm_every_dt)
    b.start()

    # initialize the led controls
    # define the used pins for the light bulbs
    rgb_pins = (17, 22, 24) 
    pwm_frequency = 50 # in Hz
    led = LED(*rgb_pins, pwm_frequency)    
    led.setup()

    # start the database and webserver
    Base.metadata.create_all(bind=engine)
    app.run(debug=True)