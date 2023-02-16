from flask import Flask,redirect,url_for,request,render_template
import pandas as pd
import pickle
import math
app=Flask(__name__)
#models
models_dictionary=pickle.load(open('model2brand.pkl','rb'))
#Car brands
l=models_dictionary.keys()

locations=['Mumbai','Pune','Chennai','Coimbatore','Hyderabad','Jaipur','Kochi','Kolkata','Delhi','Bangalore','Ahmedabad']

@app.route('/')
def home():
      #Brand
      return render_template('index.html',lst=l,loc=locations)

brand = None
@app.route('/model',methods=['POST','GET'])
def model():
      #model
      if request.method=='POST':
            brand = request.form['brand']
      return render_template('index.html',lst=l,d_lst=models_dictionary[brand],loc=locations,mdl=brand)

@app.route('/rest_feat',methods=['POST','GET'])
def rest_feat():
      model = pickle.load(open('cars_price_pred.pkl','rb'))
      modl = request.form['model']
      location = request.form['location']
      fuel = request.form['fuel']
      trans = request.form['transmission']
      owner = request.form['owner']
      year = request.form['year']
      kms = request.form['kms']
      mileage = request.form['mileage']
      engine = request.form['engine']
      power = request.form['power']
      seats = request.form['seats']
      v = model.predict(pd.DataFrame([[location,year,kms,fuel,trans,owner,mileage,engine,power,seats,brand,modl]],
columns=[ 'Location', 'Year', 'Kilometers_Driven', 'Fuel_Type',
       'Transmission', 'Owner_Type', 'Mileage', 'Engine', 'Power', 'Seats','Brands','Models']))
      return render_template('index.html',lst=l,loc=locations,res=abs(round(v[0],3)))


if __name__=='__main__':
      app.run(debug=True,port=3000)
