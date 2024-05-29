#from functools import wraps
#import sys
import os
from flask import Flask, render_template, redirect, request, url_for, session, abort
import pyrebase
import firebase_admin
from firebase_admin import credentials, firestore
import folium
import count
import math
import random
import pandas as pd
from errors.handlers import errors
import textlocal


#firebase config
config = {
  "apiKey": "AIzaSyDvmpeNYySF_cLUWzIPA4XWqJ8MEKuRNgU",
  "authDomain": "covidhelp-c2451.firebaseapp.com",
  "databaseURL": "https://covidhelp-c2451.firebaseio.com",
  "projectId": "covidhelp-c2451",
  "storageBucket": "covidhelp-c2451.appspot.com",
  "messagingSenderId": "591052628050",
  "appId": "1:591052628050:web:569bf566e80129d6f3ff8b",
  "measurementId": "G-4E9N5PNCVR"
}

#pandas
df = pd.read_csv('tirnew.csv')
#init firebase
firebase = pyrebase.initialize_app(config)
#auth instance
auth = firebase.auth()
#cloud firestore database instance
cred = credentials.Certificate("covidhelp-c2451-firebase-adminsdk-1qrdp-42309514fc.json")
firebase_admin.initialize_app(cred)
db=firestore.client()

#new instance of Flask
app = Flask(__name__)
#secret key for the session
app.secret_key = os.urandom(24)
#Blueprint registration
app.register_blueprint(errors)

#otp generation
string = "0123456789"

lent = len(string)

#folium initialization
m = folium.Map(location=[18.634974, 77.742265], zoom_start=5)

#tooltip
tooltip = 'Click here to HELP'

def flaskThread():
    app.run()

#overallPostIteration
def overAllPosts():
  # initializing python dictionary
  m = folium.Map(location=[18.634974, 77.742265], zoom_start=5)
  postDict={}
  global html_map
  #getting every users email
  posts=db.collection('users').stream()
  for post in posts:
    #getting each post
    postDict=post.to_dict()
    #condition for color variance
    if postDict['need'].upper() == 'WATER ':
      folium.Marker([postDict['latitude'], postDict['longitude']],
              popup=('<strong>Name: </strong>' + str(postDict['name']).capitalize() + '<br>'
                      '<strong>Need: </strong>' + str(postDict['need']).upper() + '<br>'
                      '<strong>Phone: </strong>' + str(postDict['phone']) ),
              icon=folium.Icon(icon='tint', color='blue'),
              tooltip=tooltip).add_to(m)
    elif postDict['need'].upper() == 'FOOD ':
      folium.Marker([postDict['latitude'], postDict['longitude']],
              popup=('<strong>Name: </strong>' + str(postDict['name']).capitalize() + '<br>'
                      '<strong>Need: </strong>' + str(postDict['need']).upper() + '<br>'
                      '<strong>Phone: </strong>' + str(postDict['phone']) ),
              icon=folium.Icon(icon='inbox ', color='orange'),
              tooltip=tooltip).add_to(m)
    elif postDict['need'].upper() == 'MEDICINE ':
      folium.Marker([postDict['latitude'], postDict['longitude']],
              popup=('<strong>Name: </strong>' + str(postDict['name']).capitalize() + '<br>'
                      '<strong>Need: </strong>' + str(postDict['need']).upper() + '<br>'
                      '<strong>Phone: </strong>' + str(postDict['phone']) ),
              icon=folium.Icon(icon='plus-sign', color='green'),
              tooltip=tooltip).add_to(m)
    elif postDict['need'].upper() == 'WATER FOOD ' or postDict['need'].upper() == 'FOOD MEDICINE ' or postDict['need'].upper() == 'WATER MEDICINE ' or postDict['need'].upper() == 'WATER FOOD MEDICINE ':
      folium.Marker([postDict['latitude'], postDict['longitude']],
              popup=('<strong>Name: </strong>' + str(postDict['name']).capitalize() + '<br>'
                      '<strong>Need: </strong>' + str(postDict['need']).upper() + '<br>'
                      '<strong>Phone: </strong>' + str(postDict['phone']) ),
              icon=folium.Icon(icon='cloud', color='red'),
              tooltip=tooltip).add_to(m)
  html_map = m.get_root().render()

#updating the map
overAllPosts()

#global jinja variable
@app.context_processor
def context_processor():
  active = count.active
  recovered = count.recovered
  death = count.death
  tot = int(active) + int(recovered)
  total = str(tot)
  return dict(a=active, r=recovered, d=death, t=total)


#home route
@app.route("/")
def home():
  return render_template("layout.html")

@app.route("/overall")
def overall():
  overAllPosts()
  return render_template("layout.html")

#index route
@app.route("/index")
def index():
  return render_template("index.html")

#create form
@app.route("/create", methods=["GET", "POST"])
def create():
  otp=""
  if request.method == "POST":
    #get the request data
    name = request.form["name"]
    need = request.form.getlist("need")
    phone=request.form["contact"]
    latitude = request.form["latitude"]
    longitude = request.form["longitude"]

    fneed=""
    for i in need:
      fneed += i + ' '

    poster = {
      "name": name,
      "need": fneed,
      "latitude": latitude,
      "longitude": longitude,
      "phone": phone,
      "author": phone
    }

    #otp generator
    for i in range(6):
      otp += string[math.floor(random.random()*lent)]

    otpmsg = 'The OTP for creating your need in Covid Essentials is: ' + otp
    #print(otpmsg)

    db.collection('otp').document(phone).set({
      "otp": otp,
    })

    db.collection('post').document(phone).set(poster)

    if(latitude=="" or longitude==""):
      return render_template("create.html", message= "Make sure to turn your location on")

    url="/userotp/"+phone

    #form validation
    if(len(name)>0 and len(fneed)>0 and len(phone)==10):
      try:
        textlocal.sendSMS('zhndVcVVvk4-n3dJee6lMpYr08iHXyNRKU8yPahT0V', '91' + phone, 'CVESSL' ,otpmsg)
        return redirect(url)
      except:
        return render_template("create.html", message= "Something wrong happened")
    else:
      return render_template("create.html", message= "* Every field must be filled and Phone number should be exactly 10 digit")
  return render_template("create.html")

#otp route
@app.route("/userotp/<id>", methods=["GET", "POST"])
def userotp(id):
  url="/userotp/"+id
  if request.method == "POST":
    userotp = request.form["otp"]
    ref=db.collection('otp').document(id).get()
    otpref=ref.to_dict()
    if otpref!=None:
      otp=otpref['otp']
    else:
      abort(403)
    pref=db.collection('post').document(id).get()
    postref=pref.to_dict()
    if postref!=None:
      poster = {
        "name": postref["name"],
        "need": postref["need"],
        "latitude": postref["latitude"],
        "longitude": postref["longitude"],
        "phone": postref["phone"],
        "author": postref["phone"],
      }
    else:
      abort(403)
    if userotp == otp:
      db.collection('otp').document(id).delete()
      db.collection('post').document(id).delete()
      try:
        db.collection('users').document(id).set(poster)
        overAllPosts()
        return redirect("/index")
      except:
        return render_template("userotp.html", message= "Something Worng happened")
    else:
      return render_template("userotp.html", message="OTP not verified")
  return render_template("userotp.html", url=url)


#map route
@app.route("/map")
def map():
  return str(html_map)
  #return render_template('map.html')

#help route
@app.route("/help")
def help():
  return render_template("help.html")

#about route
@app.route("/about")
def about():
  return render_template("about.html")

#post
@app.route("/post", methods=["GET", "POST"])
def post():
  if request.method=="POST":
    phone = request.form["contact"]
    if len(phone)==10:
      orderedDict = db.collection('users').document(phone).get()
      if orderedDict.to_dict()==None:
        return render_template("post.html", data=orderedDict.to_dict(), message="Need does not exist")
      return render_template("post.html", data=orderedDict.to_dict())
    else:
      return render_template("post.html", data=None, message="Phone number should be exactly 10 digit")
  return render_template("post.html", data=None)

#user map
@app.route("/usermap", methods=["GET", "POST"])
def usermap():
  um = folium.Map(location=[18.634974, 77.742265], zoom_start=5)
  global user_map
  if request.method == "POST":
    phone = request.form["contact"]
    if len(phone)==10:
      emailsPost = db.collection('users').document(phone).get()
      postDict=emailsPost.to_dict()
      if emailsPost.to_dict()!=None:
        if postDict['need'].upper() == 'WATER ':
          folium.Marker([postDict['latitude'], postDict['longitude']],
                  popup=('<strong>Name: </strong>' + str(postDict['name']).capitalize() + '<br>'
                          '<strong>Need: </strong>' + str(postDict['need']).upper() + '<br>'
                          '<strong>Phone: </strong>' + str(postDict['phone']) ),
                  icon=folium.Icon(icon='tint', color='blue'),
                  tooltip=tooltip).add_to(um)
        elif postDict['need'].upper() == 'FOOD ':
          folium.Marker([postDict['latitude'], postDict['longitude']],
                  popup=('<strong>Name: </strong>' + str(postDict['name']).capitalize() + '<br>'
                          '<strong>Need: </strong>' + str(postDict['need']).upper() + '<br>'
                          '<strong>Phone: </strong>' + str(postDict['phone']) ),
                  icon=folium.Icon(icon='inbox ', color='orange'),
                  tooltip=tooltip).add_to(um)
        elif postDict['need'].upper() == 'MEDICINE ':
          folium.Marker([postDict['latitude'], postDict['longitude']],
                  popup=('<strong>Name: </strong>' + str(postDict['name']).capitalize() + '<br>'
                          '<strong>Need: </strong>' + str(postDict['need']).upper() + '<br>'
                          '<strong>Phone: </strong>' + str(postDict['phone']) ),
                  icon=folium.Icon(icon='plus-sign', color='green'),
                  tooltip=tooltip).add_to(um)
        elif postDict['need'].upper() == 'WATER FOOD ' or postDict['need'].upper() == 'FOOD MEDICINE ' or postDict['need'].upper() == 'WATER MEDICINE ' or postDict['need'].upper() == 'WATER FOOD MEDICINE ':
          folium.Marker([postDict['latitude'], postDict['longitude']],
                  popup=('<strong>Name: </strong>' + str(postDict['name']).capitalize() + '<br>'
                          '<strong>Need: </strong>' + str(postDict['need']).upper() + '<br>'
                          '<strong>Phone: </strong>' + str(postDict['phone']) ),
                  icon=folium.Icon(icon='cloud', color='red'),
                  tooltip=tooltip).add_to(um)
      else:
        user_map = um.get_root().render()
        return render_template('usermap.html', message="Need does not exist", map=user_map)
    else:
      user_map = um.get_root().render()
      return render_template('usermap.html', message="Phone number must be exactly 10 digit", map=user_map)
  user_map = um.get_root().render()
  return render_template("usermap.html", map=user_map)

#needs satisfied
@app.route('/needsat')
def satneed():
  tm = folium.Map(location=[11.206088, 77.270105], zoom_start=10)
  for i in range(99):
    loc = df['LOCATION'][i].split(', ')
    if str(df['STATE'][i]).upper() == 'ANDHRA PRADESH':
      folium.Marker([loc[0], loc[1]],
                popup='<h4><strong>Name: </strong>' + str(df['NAME'][i]).capitalize() + '<br>'
                        '<strong>Age: </strong>' + str(df['AGE'][i]) + '<br>'
                        '<strong>Native: </strong>' + str(df['STATE'][i]).capitalize() + '<br>'
                        '<strong>Mobile: </strong>' + str(df['MOBILE'][i]) + '</h4>',
                icon=folium.Icon(icon='plus-sign', color='orange'),
                tooltip=tooltip).add_to(tm)
    elif str(df['STATE'][i]).upper() == 'RAJASTHAN':
      folium.Marker([loc[0], loc[1]],
                popup='<h4><strong>Name: </strong>' + str(df['NAME'][i]).capitalize() + '<br>'
                        '<strong>Age: </strong>' + str(df['AGE'][i]) + '<br>'
                        '<strong>Native: </strong>' + str(df['STATE'][i]).capitalize() + '<br>'
                        '<strong>Mobile: </strong>' + str(df['MOBILE'][i]) + '</h4>',
                icon=folium.Icon(icon='plus-sign', color='green'),
                tooltip=tooltip).add_to(tm)
    elif str(df['STATE'][i]).upper() == 'KERALA':
      folium.Marker([loc[0], loc[1]],
                popup='<h4><strong>Name: </strong>' + str(df['NAME'][i]).capitalize() + '<br>'
                        '<strong>Age: </strong>' + str(df['AGE'][i]) + '<br>'
                        '<strong>Native: </strong>' + str(df['STATE'][i]).capitalize() + '<br>'
                        '<strong>Mobile: </strong>' + str(df['MOBILE'][i]) + '</h4>',
                icon=folium.Icon(icon='plus-sign', color='yellow'),
                tooltip=tooltip).add_to(tm)
    elif str(df['STATE'][i]).upper() == 'WEST BENGAL':
      folium.Marker([loc[0], loc[1]],
                popup='<h4><strong>Name: </strong>' + str(df['NAME'][i]).capitalize() + '<br>'
                        '<strong>Age: </strong>' + str(df['AGE'][i]) + '<br>'
                        '<strong>Native: </strong>' + str(df['STATE'][i]).capitalize() + '<br>'
                        '<strong>Mobile: </strong>' + str(df['MOBILE'][i]) + '</h4>',
                icon=folium.Icon(icon='plus-sign', color='blue'),
                tooltip=tooltip).add_to(tm)
    elif str(df['STATE'][i]).upper() == 'PUNJAB':
      folium.Marker([loc[0], loc[1]],
                popup='<h4><strong>Name: </strong>' + str(df['NAME'][i]).capitalize() + '<br>'
                        '<strong>Age: </strong>' + str(df['AGE'][i]) + '<br>'
                        '<strong>Native: </strong>' + str(df['STATE'][i]).capitalize() + '<br>'
                        '<strong>Mobile: </strong>' + str(df['MOBILE'][i]) + '</h4>',
                icon=folium.Icon(icon='plus-sign', color='red'),
                tooltip=tooltip).add_to(tm)
    elif str(df['STATE'][i]).upper() == 'MAHARASHTRA':
      folium.Marker([loc[0], loc[1]],
                popup='<h4><strong>Name: </strong>' + str(df['NAME'][i]).capitalize() + '<br>'
                        '<strong>Age: </strong>' + str(df['AGE'][i]) + '<br>'
                        '<strong>Native: </strong>' + str(df['STATE'][i]).capitalize() + '<br>'
                        '<strong>Mobile: </strong>' + str(df['MOBILE'][i]) + '</h4>',
                icon=folium.Icon(icon='plus-sign', color='pink'),
                tooltip=tooltip).add_to(tm)
    elif str(df['STATE'][i]).upper() == 'UTTAR PRADESH':
      folium.Marker([loc[0], loc[1]],
                popup='<h4><strong>Name: </strong>' + str(df['NAME'][i]).capitalize() + '<br>'
                        '<strong>Age: </strong>' + str(df['AGE'][i]) + '<br>'
                        '<strong>Native: </strong>' + str(df['STATE'][i]).capitalize() + '<br>'
                        '<strong>Mobile: </strong>' + str(df['MOBILE'][i]) + '</h4>',
                icon=folium.Icon(icon='plus-sign', color='purple'),
                tooltip=tooltip).add_to(tm)
    elif str(df['STATE'][i]).upper() == 'KARNATAKA':
      folium.Marker([loc[0], loc[1]],
                popup='<h4><strong>Name: </strong>' + str(df['NAME'][i]).capitalize() + '<br>'
                        '<strong>Age: </strong>' + str(df['AGE'][i]) + '<br>'
                        '<strong>Native: </strong>' + str(df['STATE'][i]).capitalize() + '<br>'
                        '<strong>Mobile: </strong>' + str(df['MOBILE'][i]) + '</h4>',
                icon=folium.Icon(icon='plus-sign', color='gray'),
                tooltip=tooltip).add_to(tm)
  tir_map = tm.get_root().render()
  return render_template('needsat.html', mapt=tir_map)

#delete function
@app.route("/delete", methods=["GET", "POST"])
def delete():
    deleteotp = ""
    if request.method=="POST":
      deletephone = request.form["contact"]
      deletePost=db.collection('users').document(deletephone).get()
      if deletePost.to_dict()!=None:
        for i in range(6):
          deleteotp += string[math.floor(random.random()*lent)]
        otpmsg = 'The OTP for creating your need in Covid Essentials is: ' + deleteotp
        #print(otpmsg)
        db.collection('deleteotp').document(deletephone).set({
          "deleteotp": deleteotp,
        })
        deleteurl="/deleteuserotp/"+deletephone
        try:
          textlocal.sendSMS('zhndVcVVvk4-n3dJee6lMpYr08iHXyNRKU8yPahT0V', '91' + deletephone, 'CVESSL' ,otpmsg)
          return redirect(deleteurl)
        except:
          return render_template("delete.html", message= "Something wrong happened")
      else:
        return render_template("delete.html", message= "No need exists")
    return render_template('delete.html')

#delete otp
@app.route("/deleteuserotp/<id>", methods=["GET", "POST"])
def deleteuserotp(id):
  deleteurl="/deleteuserotp/"+id
  if request.method == "POST":
    deleteotp=""
    userotp = request.form["otp"]
    deleteoptref=db.collection('deleteotp').document(id).get()
    if deleteoptref.to_dict()!=None:
      ref=deleteoptref.to_dict()
      deleteotp=ref['deleteotp']
    else:
      abort(403)
    if userotp == deleteotp:
      db.collection('deleteotp').document(id).delete()
      try:
        db.collection('users').document(id).delete()
        overAllPosts()
        return redirect("/")
      except:
        return render_template("deleteuserotp.html", message= "Something Worng happened")
    else:
      return render_template("deleteuserotp.html", message="OTP not verified")
  return render_template("deleteuserotp.html", url=deleteurl)

#run the main script
if __name__ == "__main__":
    app.run(debug=True)