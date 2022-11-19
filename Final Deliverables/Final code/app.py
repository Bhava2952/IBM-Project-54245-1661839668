import secrets
from turtle import title
from unicodedata import category
from flask import Flask, render_template, request, redirect, url_for, session
import ibm_db
from connect import *
from flask_mail import Mail,Message
import bcrypt
import base64
import os
import random


app = Flask(__name__)


@app.route("/", methods=["GET"])
def login():
    return render_template("signin.html")



@app.route("/admin", methods=["GET"])
def admin():
    return render_template("admin.html")

@app.route("/best/", methods=["GET"])
def best():
          if not session.get("name"):
           return redirect("/")
          sql = "SELECT * FROM PROD_TBL"
          stmt1 = ibm_db.exec_immediate(conn, sql)
          row = ibm_db.fetch_assoc(stmt1)
          print(row)
          prodname = []
          prodprice = []
          prodimg = []
          while row != False:
            print (row["PROD_NAME"])
            prodname.append(row["PROD_NAME"])
            prodprice.append(row['PROD_PRICE'])
            prodimg.append(row['PRO_IMG'])
            row = ibm_db.fetch_assoc(stmt1)
          return render_template ( "bestdeals.html" , len = len(prodname), prodname = prodname,prodprice=prodprice,prodimg=prodimg)

@app.route("/male/", methods=["GET"])
def male():
          if not session.get("name"):
            return redirect("/")
          sql = "SELECT * FROM PROD_TBL WHERE PRO_CAT = 'Male'"
          stmt1 = ibm_db.exec_immediate(conn, sql)
          row = ibm_db.fetch_assoc(stmt1)
          print(row)
          prodname = []
          prodprice = []
          prodimg = []
          while row != False:
            print (row["PROD_NAME"])
            prodname.append(row["PROD_NAME"])
            prodprice.append(row['PROD_PRICE'])
            prodimg.append(row['PRO_IMG'])
            row = ibm_db.fetch_assoc(stmt1)
          return render_template ( "maleshop.html" , len = len(prodname), prodname = prodname,prodprice=prodprice,prodimg=prodimg)

@app.route("/Female/", methods=["GET"])
def female():
          if not session.get("name"):
            return redirect("/")
          sql = "SELECT * FROM PROD_TBL WHERE PRO_CAT = 'Female'"
          stmt1 = ibm_db.exec_immediate(conn, sql)
          row = ibm_db.fetch_assoc(stmt1)
          print(row)
          prodname = []
          prodprice = []
          prodimg = []
          while row != False:
            print (row["PROD_NAME"])
            prodname.append(row["PROD_NAME"])
            prodprice.append(row['PROD_PRICE'])
            prodimg.append(row['PRO_IMG'])
            row = ibm_db.fetch_assoc(stmt1)
          return render_template ( "Femaleshop.html" , len = len(prodname), prodname = prodname,prodprice=prodprice,prodimg=prodimg)

@app.route("/logged/",methods=["POST"])
def logged():
    user = request.form["user"].lower()
    pwd = request.form["pwd"]
    logged.mailid = user
    if user == "" or pwd == "":
        return render_template ( "login.html" )
    query = "SELECT * FROM USER_TBL WHERE username = '"+user+"' AND password = '"+pwd+"'"
    stmt = ibm_db.exec_immediate(conn, query)
    rows = ibm_db.fetch_assoc(stmt)
    try:
      if len(rows) == 2:
          session["name"] = user
          print('ok')
          return redirect("/shop/")
      else:
          return render_template ( "login.html", msg="Wrong username or password." )
    except:
       return render_template ( "login.html", msg="Wrong username or password." )

@app.route("/loggedad/",methods=["POST"])
def loggedad():
    user = request.form["user"]
    pwd = request.form["pwd"]
    if user == "" or pwd == "":
        return render_template ( "login.html" )
    query5 = "SELECT * FROM ADMIN_TBL WHERE username = '"+user+"' AND password = '"+pwd+"'"
    stmt5 = ibm_db.exec_immediate(conn, query5)
    rows5 = ibm_db.fetch_assoc(stmt5)
    print(rows5)
    try:
      session["name"] = user
      if len(rows5) == 2:
          print('ok')
          return redirect("/add/")
      else:
          return render_template ( "admin.html", msg="Wrong username or password." )
    except:
       return render_template ( "admin.html", msg="Wrong username or password." )


@app.route("/shop/" , methods=['GET'])
def shop():
          if not session.get("name"):
           return redirect("/")
          sql = "SELECT * FROM PROD_TBL"
          stmt1 = ibm_db.exec_immediate(conn, sql)
          row = ibm_db.fetch_assoc(stmt1)
          print(row)
          prodname = []
          prodprice = []
          prodimg = []
          while row != False:
            print (row["PROD_NAME"])
            prodname.append(row["PROD_NAME"])
            prodprice.append(row['PROD_PRICE'])
            prodimg.append(row['PRO_IMG'])
            row = ibm_db.fetch_assoc(stmt1)

          return render_template ( "index.html" , len = len(prodname), prodname = prodname,prodprice=prodprice,prodimg=prodimg)

@app.route("/Order/" , methods=['GET'])
def order():
          if not session.get("name"):
           return redirect("/")          
          sql = "SELECT * FROM ORDHIST_TBL Where PUR_MAIL = '"+logged.mailid+"'"
          stmt2 = ibm_db.exec_immediate(conn, sql)
          row = ibm_db.fetch_assoc(stmt2)
          print(row)
          prod_name = []
          pur_date = []
          pur_mail = []
          while row != False:
            print (row["PROD_NAME"])
            prod_name.append(row["PROD_NAME"])
            pur_date.append(row['PUR_DATE'])
            pur_mail.append(row['PUR_MAIL'])
            row = ibm_db.fetch_assoc(stmt2)

          return render_template ( "cart.html" , len = len(prod_name), prod_name = prod_name,purc_date=pur_date,purc_mail=pur_mail)
@app.route("/Orderhis/" , methods=['GET'])
def orderhis():
          if not session.get("name"):
           return redirect("/")  
          sql = "SELECT * FROM ORDHIST_TBL"
          stmt2 = ibm_db.exec_immediate(conn, sql)
          row = ibm_db.fetch_assoc(stmt2)
          print(row)
          prod_name = []
          pur_date = []
          pur_mail = []
          while row != False:
            print (row["PROD_NAME"])
            prod_name.append(row["PROD_NAME"])
            pur_date.append(row['PUR_DATE'])
            pur_mail.append(row['PUR_MAIL'])
            row = ibm_db.fetch_assoc(stmt2)

          return render_template ( "orderhis.html" , len = len(prod_name), prod_name = prod_name,purc_date=pur_date,purc_mail=pur_mail)



@app.route("/add/", methods=["GET"])
def add():
          if not session.get("name"):
           return redirect("/")
          return render_template("addproduct.html")


@app.route("/logout/", methods=["GET"])
def logout():
     session["name"] = None
     return render_template("signin.html")

@app.route("/register/", methods=["GET"])
def register():
     return render_template("signup.html")

@app.route("/registered/", methods=["POST"])
def registered():
     username = request.form["username"]
     password = request.form["pass"] 
     sql2 = "insert into USER_TBL values(?,?)"
     stmt7 = ibm_db.prepare(conn, sql2)
     ibm_db.bind_param(stmt7, 1, username)
     ibm_db.bind_param(stmt7, 2, password)
     try:
      ibm_db.execute(stmt7)
      return render_template("login.html",msg = "Added Successfully")
     except:
       print(ibm_db.stmt_errormsg())
       return render_template("Register.html",msg = "tryagin")



@app.route("/added/", methods=["POST"])
def added():
  prod_name = request.form["prodname"]
  prod_price = request.form["prodprice"] 
  prod_cat = request.form["prodcat"]
  prod_img = request.form["prodimg"]
  sql1 = "insert into PROD_TBL values(?,?,?,?)"
  stmt6 = ibm_db.prepare(conn, sql1)
  ibm_db.bind_param(stmt6, 1, prod_name)
  ibm_db.bind_param(stmt6, 2, prod_price)
  ibm_db.bind_param(stmt6, 3, prod_img)
  ibm_db.bind_param(stmt6, 4, prod_cat)
  try:
    ibm_db.execute(stmt6)
    return render_template("addproduct.html",msg = "Added Successfully")
  except:
    print(ibm_db.stmt_errormsg())
    return render_template("addproduct.html",msg = "tryagin")

if __name__ == "__main__":
    app.run(host='0.0.0.0')