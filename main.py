from flask import Flask, render_template, request, redirect, url_for
import os
from os.path import join, dirname, realpath

import pandas as pd
import mysql.connector

app = Flask(__name__)

# Upload folder
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] =  UPLOAD_FOLDER


# Database
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="csvTodatabase"
)

mycursor = mydb.cursor()

# Root URL
@app.route('/')
def index():
    return render_template('index.html')


# Get the uploaded files
@app.route("/upload", methods=['POST'])
def uploadFiles():
      # get the uploaded file
      uploaded_file = request.files['file']
      if uploaded_file.filename != '':
           file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
          # set the file path
           uploaded_file.save(file_path)
           print(file_path)
           parseCSV(file_path)
          # save the file
      return redirect(url_for('index'))

# To show the Database
@app.route("/show", methods=['POST'])
def showDatabase():
      mycursor.execute("SELECT product_id,product_name,price FROM product")
      data = mycursor.fetchall()
      return render_template('display.html', data=data)

def parseCSV(filePath):
      col_names = ['product_id','product_name','price']
      # Using Pandas to parse the CSV file
      csvData = pd.read_csv(filePath,names=col_names, header=None)
      # Loop through the Rows
      for i,row in csvData.iterrows():
             sql = "INSERT INTO product (product_id, product_name, price) VALUES (%s, %s, %s)"
             value = (row['product_id'],row['product_name'],row['price'])
             mycursor.execute(sql, value)
             mydb.commit()

if (__name__ == "__main__"):
     app.run(port = 5000)
