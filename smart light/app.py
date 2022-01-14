from flask import Flask,render_template,request,redirect,url_for,session,flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.dialects.mysql import TIME
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
class lichtan(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    licht = db.Column("licht", db.Integer)
    def __init__(self, licht):
        self.licht = licht

class licht(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    zeit = db.Column("zeit", db.String)

    def __init__(self, zeit):
        self.zeit = zeit
@app.route("/licht", methods=["POST", "GET"])
def lichtein():
      if request.method == "POST":
        session.permanent = True
        licht = request.form["licht"]
        session["licht"] = licht
        lichtein = lichtan.query.filter_by(licht=licht).first()
        if lichtein:
            session["licht"] =lichtein.licht
        else:
            light = lichtan(licht)
            db.session.add(light)
            db.session.commit()


        flash("Licht ist an!")
        return redirect(url_for("lichtein"))
      else:
        if "licht" in session: 
            flash("Licht ist bereits an!")
            return redirect(url_for("weckerstellen"))
        return render_template("licht.html")

@app.route("/wecker", methods=["POST", "GET"])
def weckerstellen():
    if request.method == "POST":
        session.permanent = True
        zeit = request.form["wecker"]
        session["zeit"] = zeit
        found_wecker = licht.query.filter_by(zeit=zeit).first()
        if found_wecker:
            session["zeit"] =found_wecker.zeit
        else:
            zeitpunkt = licht(zeit)
            db.session.add(zeitpunkt)
            db.session.commit()


        flash("Wecker wurde erfolgreich gestellt!")
        return redirect(url_for("weckeranzeige"))
    else:
        # if "zeit" in session: 
        #     flash("Der Wecker war bereits gestellt!")
        #     return redirect(url_for("weckeranzeige"))
        return render_template("wecker.html")
def lichtein():
      if request.method == "POST":
        session.permanent = True
        licht = request.form["licht"]
        session["licht"] = licht
        lichtein = lichtan.query.filter_by(licht=licht).first()
        if lichtein:
            session["licht"] =lichtein.licht
        else:
            light = lichtan(licht)
            db.session.add(light)
            db.session.commit()


        flash("Licht ist an!")
        return redirect(url_for("lichtein"))
      else:
        if "licht" in session: 
            flash("Licht ist bereits an!")
            return redirect(url_for("weckerstellen"))
        return render_template("licht.html")
@app.route("/anzeige")
def weckeranzeige():
  
 return render_template("weckeranzeige.html", values=licht.query.all())

@app.route("/lichtaus")
def lichtaus():
        flash(f"Licht wird ausgeschalten", "info")
        session.pop("lichtaus", None)
        return redirect(url_for("weckerstellen"))



@app.route("/loeschen", methods=["GET", "POST"])
def weckerentfernen():
    
    if "zeit" in session:
        zeit = session["zeit"]

        if request.method == "POST":
            session.permanent = True
            return request.form.getlist['loeschen']
            session["zeit"] = zeit
            found_zeit = licht.query.filter_by(zeit=zeitloeschen).delete()
           # db.session.delete(found_zeit)
            db.session.commit()
            flash(f"Wecker was deleted: {zeit}")
        else:
            if "zeit" in session:
                zeit = session["zeit"]
                return render_template("weckerentfernen.html", values=licht.query.all())
  
    else:
        flash("You are not logged in!")
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
    db.create_all()
    app.run(debug=True)