
#code v3

from flask import Flask, request, jsonify,send_file
from flask import redirect, url_for
import re
from flask_login import login_user,login_required, LoginManager, UserMixin
from flask_login import LoginManager



from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os
import io
from flask import session
from dotenv import load_dotenv

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import statsmodels.api as sm
import numpy as np
from sklearn.metrics import r2_score
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.neighbors import KNeighborsRegressor
import matplotlib.pyplot as plt
from matplotlib import pyplot as plt
import matplotlib

matplotlib.use('Agg')
app = Flask(__name__)
CORS(app)
login_manager = LoginManager(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///signup.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

load_dotenv()
SECRET_KEY = os.environ.get('SECRET_KEY', 'your_secret_key')
app.secret_key = 'your_secret_key'

# SECRET_KEY = 'my-sec'
from app import db
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    def is_active(self):
        return True
    def get_id(self):
        return str(self.id)


with app.app_context():
    db.create_all()



@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data['username']
    password = data['password']
    email = data['email']
    emailc = '^[a-z0-9]+[\._]?[ a-z0-9]+[@]\w+[. ]\w{2,3}$'
    checkuser = User.query.filter_by(email=email).first()
    

    if username == '' or email == '' or password == '':
        return jsonify({'message' : 'All the fields are required'})
    elif not re.match(emailc,email):
        return jsonify({'error': 'Invalid Email Adress'})
    elif checkuser:
        return jsonify({'error': 'Account already exists'})
    elif len(password)<8:
        return jsonify({'error': 'The Password should contain atleast 8 characters'})
    else:
        # return jsonify({'message': 'User signed up successfully!'})
        userdb = User(username= username, email = email,password=password)
        db.session.add(userdb)
        db.session.commit()
        if checkuser:
            login_user(checkuser, remember=True)
        return jsonify({'message': 'User created successfully'})


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']
    user = User.query.filter_by(username=username, password=password).first()

    if username == '' or password == '':
        return jsonify({'error': 'Fill the required field'}) 
    elif user:
        if user.password == password:
            login_user(user, remember=True)
            return jsonify({'message': 'Login successful'})
        else:
            return jsonify({'error': 'Invalid Password'})
    else:
        return jsonify({'error': 'Invalid Username Or Password'})

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload', methods=['POST'])
def upload():
    
    if 'file' not in request.files:
        return jsonify({'error': 'No file found'})
    file = request.files['file']
    selectcheck = request.form['selectcheck'] 
    print(selectcheck)

    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    df = pd.read_csv(file_path)
    # print(df.head())
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    df['Order Date'] = df['Order Date'].dt.strftime('%d/%m/%Y')
    df['Order Date'] = pd.to_datetime(df['Order Date'], format='%d/%m/%Y')
    df['Order Date'] = pd.to_datetime(df['Order Date'], format='%m/%d/%Y')
    df['month'] = df['Order Date'].dt.month
    df['year'] = df['Order Date'].dt.year
    df['week'] = df['Order Date'].dt.isocalendar().week
    df['day'] = df['Order Date'].dt.day
    monthlysales = df.groupby(['year', 'month']).agg({'Sales': 'sum'}).reset_index()
    monthlysales['Sales'] = monthlysales['Sales']
    df['year_month'] = pd.to_datetime(df['year'].astype(str) + '-' + df['month'].astype(str), format='%Y-%m')

    weeklysales = df.groupby(['year', 'week']).agg({'Sales': 'sum'}).reset_index()

    dailysales = df.groupby(['year', 'month', 'day']).agg({'Sales': 'sum'}).reset_index()

    if selectcheck == 'yearly':
        yearfrom = int(request.form['yearFrom'])
        yearto = int(request.form['yearTo'])
        x = monthlysales[['year', 'month']]
        y = monthlysales['Sales']
        x_train, x_test, y_train, y_test = train_test_split(x, y, train_size=0.7, random_state=0)
        model = KNeighborsRegressor()
        model.fit(x_train, y_train)
        pred = model.predict(x_test)
        l = []
        year = []
        salesy = []
        # yearly
        a = yearfrom
        for i in range(0, yearto):
            l1 = []
            for j in range(1, 13):  
                l1.append(model.predict([[a, j]]))
            year.append(a)
            a += 1
            l.append(l1)
        for i in l:
            for i in sum(i):
                salesy.append(round(i,3))
        yearly = pd.DataFrame({'year': year, 'sales': salesy})
        fname = 'prediction.csv'
        path = 'static/uploads'
        file1 = os.path.join(path, fname)
        yearly.to_csv(file1, index=False)
        return jsonify({"success": 'successful'})
    elif selectcheck == 'monthly':
        yearmonthly = int(request.form['yearForMonthly'])
        numMonthly = int(request.form['numForMonthly'])
        a = yearmonthly
        x = monthlysales[['year', 'month']]
        y = monthlysales['Sales']
        x_train, x_test, y_train, y_test = train_test_split(x, y, train_size=0.7, random_state=0)
        model = KNeighborsRegressor()
        model.fit(x_train, y_train)
        pred = model.predict(x_test)        
        month = ['Jan ' + str(a), 'Feb ' + str(a), 'Mar ' + str(a), 'Apr ' + str(a), 'May ' + str(a), 'Jun ' + str(a), 'Jul ' + str(a), 'Aug ' + str(a), 'Sep ' + str(a), 'Oct ' + str(a), 'Nov ' + str(a), 'Dec ' + str(a)]
        salesm = []
        for i in range(1, numMonthly):
            for j in model.predict([[a, i]]):
                salesm.append(round(j,3))
        mon = month[:numMonthly-1]
        monthly = pd.DataFrame({'month': mon, 'sales': salesm})
        fname = 'prediction.csv'
        path = 'static/uploads'
        file1 = os.path.join(path, fname)
        monthly.to_csv(file1, index=False)
        return jsonify({"success": 'successful'})
    elif selectcheck == 'weekly':
        yearweekly = int(request.form['yearForweekly'])
        numweekly = int(request.form['numForweekly'])
        x = weeklysales[['year','week']]
        y =weeklysales['Sales']
        x_train,x_test,y_train,y_test = train_test_split(x,y,train_size =0.7, random_state= 0)
        model = KNeighborsRegressor()
        model.fit(x_train,y_train)
        pred = model.predict(x_test)
        a = yearweekly
        wsales=[]
        weekno=[]
        for i in range(1,numweekly):
            weekno.append('week '+str(i))
            for j in (model.predict([[a,i]])):
                wsales.append(round(j,3))
        weeksales = pd.DataFrame({'week':weekno,'sales': wsales})
        fname = 'prediction.csv'
        path = 'static/uploads'
        file1 = os.path.join(path, fname)
        weeksales.to_csv(file1, index=False)
        return jsonify({"success": 'successful'})

    elif selectcheck == 'daily':
        yeardaily = int(request.form['yearForDaily'])
        monthdaily = int(request.form['monthForDaily'])
        dayDaily= int(request.form['dayForDaily'])
        x = dailysales[['year','month','day']]
        y =dailysales['Sales']
        x_train,x_test,y_train,y_test = train_test_split(x,y,train_size =0.7, random_state= 0)
        model = KNeighborsRegressor()
        model.fit(x_train,y_train)
        pred = model.predict(x_test)
        a = yeardaily
        b= monthdaily
        dsales=[]
        dayno=[]
        for i in range(1,dayDaily):
            dayno.append('Day '+str(i))
            for j in (model.predict([[a,b,i]])):
                dsales.append(round(j,3))
        dailys = pd.DataFrame({'Day':dayno[:dayDaily-1],'sales': dsales})
        fname = 'prediction.csv'
        path = 'static/uploads'
        file1 = os.path.join(path, fname)
        dailys.to_csv(file1, index=False)
        return jsonify({"success": 'successful'})

    
@app.route('/powerbi', methods=['GET','POST'])
def powerbi_endpoint():
    data = request.get_json()
    a = data.get('a')
    file_path = os.path.join('static/uploads', 'prediction.csv')
    df1 = pd.read_csv(file_path)
    chartdata = df1.iloc[:, [0, 1]]
    chartlabels = chartdata.iloc[:, 0].tolist()
    chartvalues = chartdata.iloc[:, 1].tolist()
    plt.figure()
    plt.plot(chartlabels, chartvalues)

    if chartdata.columns[0]=="year":
        plt.xlabel('Years')
        plt.title('SALES FOR YEAR')
    elif chartdata.columns[0]=="month":
        plt.xlabel("Months")
        plt.title('SALES FOR MONTH')

    elif chartdata.columns[0]=="week":
        plt.xlabel('Weeks')
        plt.title('SALES FOR WEEK')
    else:
        plt.xlabel('Days')
        plt.title('SALES FOR DAYS')
    plt.ylabel('Sales')
    chartimagepath = os.path.join(r'E:/Final Project/salesforecasting/salesforecast/sales/src/assets', 'chart.png')
    plt.savefig(chartimagepath)
    plt.close()
    
    plt.figure()   
    plt.bar(chartlabels, chartvalues)
    chartimagepath1 = os.path.join(r'E:/Final Project/salesforecasting/salesforecast/sales/src/assets', 'chart1.png')
    plt.savefig(chartimagepath1)
    plt.close()

    responsedata = {
        'chartlabels': chartlabels,
        'chartvalues': chartvalues
    }

    return jsonify(responsedata)
    

@app.route('/', methods=['GET'])
def index():
    return 'Sales Forecasting'
    
if __name__ == '__main__':
    app.run(debug=True)
