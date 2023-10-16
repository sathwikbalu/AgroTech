from flask import Flask,redirect,url_for,render_template,request,flash
from flask_sqlalchemy import SQLAlchemy
import random
import requests
import smtplib
import ssl
from email.message import EmailMessage
from flask_login import login_user,current_user,logout_user,login_required
app = Flask(__name__)
app.config['SECRET_KEY']='sath10hemu15prab17'
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///sathwik.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
with app.app_context():
    db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(15),nullable=False)
    email=db.Column(db.String(60),nullable=False)
    password=db.Column(db.String(60),nullable=False)
    location=db.Column(db.String(60),nullable=False)

    def __repr__(self)  ->str:
        return f"('{self.id}','{self.username}','{self.email}','{self.password}','{self.location}')"

Location=str()
@app.route("/")
def main():
    return render_template("main.html")


@app.route("/login",methods=['GET','POST'])
def login():
    global Location
    if request.method=='POST':
        email=(request.form['email'])
        password=(request.form['password'])
        user = User.query.filter_by(email=email).first()
        Location=(user.location)
        if user:
            password_w = user.password
            if password==password_w:
                flash(f'You are logged into {user.username}', 'success')
                return redirect('/weather')
            else:
                flash("Password is incorrect!",'warning')
        else:
            flash("Email Id doesn't Exist", 'warning')


    return render_template("login.html")


@app.route("/register" ,methods=['GET','POST'])
def register():
    if request.method=="POST":
        username=(request.form['username'])
        email=(request.form['email'])
        password=(request.form['password'])
        confrim_password=(request.form['confrim_password'])   
        location=(request.form['location'])
        user_name = User.query.filter_by(username=username).first()
        user_email = User.query.filter_by(email=email).first()
        if user_name:
            flash('Username already taken!', 'warning')
        elif user_email:
            flash('Email address already registered', 'warning')
        elif password==confrim_password:
            user = User(username=username,email=email,password=password,location=location) 
            # db.create_all()
            db.session.add(user)
            db.session.commit()
            flash('Your account has been created!','success')
            return redirect('/login')
        
        else:
            flash("Password Doesn't Match",'danger')
    return render_template("register.html")


@app.route("/secound")
def second():
    return render_template("Secondpage.html")

OTP = ''.join([str(random.randint(0,9)) for i in range(4)])
@app.route("/forgetpassword",methods=['GET','POST'])
def forgetpass():
    if request.method=='POST':
        mailid =(request.form["email"])
        generate_otp(mailid)
        return redirect('/otp')
    return render_template("forgetPass.html")


@app.route("/otp",methods=['GET','POST'])
def Otp():
    if request.method=='POST':
        mailid =(request.form["email"])
        otp_c = (request.form['otp'])
        location = (request.form['location'])
        new_pass=(request.form["new_password"])
        confrim_pass=(request.form["confrim_password"])
        if OTP==otp_c:
            user = User.query.filter_by(email=mailid).first()
            if new_pass==confrim_pass:
                user.email=mailid
                user.password = new_pass
                user.location = location
                db.session.add(user)
                db.session.commit()
                flash("Password changed Successfully",'sucess')
                return redirect('/login')
            else :
                flash ("Password and confirm Password should be same!")
        else:
            flash("Otp is Incorrect","warning")
    return render_template("otp.html")


def generate_otp(mailid):
    email_sender = 'dlsathwik@gmail.com'
    email_password = 'wnfppwzpxswzryqy'
    email_receiver =  mailid
    car=smtplib.SMTP("smtp.gmail.com",587)
    car.starttls()
    car.login(email_sender,email_password)
    car.sendmail(from_addr=email_sender,to_addrs=email_receiver,msg=f"Your Otp for forget password {OTP}(Dont share to anyone)")
    car.close()
    return 

@app.route("/weather")
def weather():
    return render_template("weather.html")


@app.route("/aboutus")
def aboutus():
    return render_template("aboutus.html")

@app.route("/feedback")
def feedback():
    return render_template("feedback.html")


@app.route("/payment")
def payment():
    return render_template("payment.html")


@app.route("/sensor")
def sensor():
    return render_template("sensor.html")

@app.route("/npk")
def npk():
    return render_template("npk.html")

@app.route("/npkrev")
def npkrev():
    return render_template("npkrev.html")

@app.route("/dispwea")
def dispwea():
    global Location
    API_KEY = 'c17516d078812be0a1975acab68acb44'
    BASE_URL = 'https://api.openweathermap.org/data/2.5/forecast'
    def get_weather_data(location_name):
        params = {
            'q': location_name,
            'appid': 'c17516d078812be0a1975acab68acb44',
            'units': 'metric',  # Use 'imperial' for Fahrenheit
            'cnt': 17 ,  # Number of days (up to 5) for the forecast
        }

        response = requests.get(BASE_URL, params=params)

        if response.status_code == 200:
            return response.json()
        else:
            # print("Error fetching weather data.")
            return None
    try:    
        location_name = Location
        weather_data = get_weather_data(location_name)
        if weather_data:
            #
            return render_template('dispwea.html',weather_data=weather_data)
    except:
        flash('Unable To Load The Weather Data!','danger')
    return render_template("dispwea.html")


@app.route("/agroforestry")
def agroforestry():
    return render_template("agroforestry.html")

@app.route("/consagriculture")
def consagriculture():
    return render_template("consagriculture.html")

@app.route("/covercropsandmulching")
def covercropsandmulching():
    return render_template("covercropsandmulching.html")


@app.route("/sorintensification")
def sorintensification():
    return render_template("sorintensification.html")

@app.route("/vermicomposting")
def vermicomposting():
    return render_template("vermicomposting.html")

@app.route("/naturalfarming")
def naturalfarming():
    return render_template("natural farming.html")

@app.route("/orgfarming")
def orgfarming():
    return render_template("org farming.html")

@app.route("/precfarmi")
def precfarmi():
    return render_template("precfarmi.html")

@app.route("/integratedpestmanagement")
def integratedpestmanagement():
    return render_template("integratedpestmanagement.html")

if (__name__=="__main__"):

    app.run(debug=True,port=8000)