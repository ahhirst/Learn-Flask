from flask import Flask, flash, render_template, request, redirect, url_for, session
import mysql.connector
from mysql.connector import Error
from datetime import timedelta
from modules import *
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = '12688fuy234y512cy5c12ucf'  # Secret key for session management
app.permanent_session_lifetime = timedelta(minutes=10)  # Set session lifetime to 7 days


@app.route("/", methods=["GET", "POST"])
def login():
    print("login")
    if 'username' in session:
        return redirect(url_for('index'))
    if request.method == "POST":
        name = request.form.get("name")
        password = request.form.get("password")
        if name and password and check_name_pass(name, password):
            session.permanent = True  # Make the session permanent
            session['username'] = name
            return redirect(url_for('index'))
        else:
            flash('Invalid Username or Password !!', 'warning')  # Flash message for unauthorized access

            return redirect(url_for('login'))
            # return "<h1>Invalid credentials</h1>"
    return render_template("login.html")

@app.route("/index", methods=["GET", "POST"])
def index():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    allstd, columns = all_student()
    search = None
    combined = []
    
    if request.method == "POST":
        try:
            name = request.form.get("name")
            search = one_student(name)
            if not search:
                flash (f"Not Found Name {name}")
                return redirect(url_for('index'))
            print(allstd)
            combined = zip(columns,search)

        except KeyError:
            print("Error: 'name' field is missing in the form data")
            return "<h1>Form data error</h1>"
        except Error as e:
            print(f"Error processing form data: {e}")
            return "<h1>Internal Server Error</h1>"
    return render_template("index.html", columns=columns, data=allstd,combined=combined, search=search)



@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))
@app.route("/update", methods=["GET", "POST"])
def update_password_route():
    
    if request.method == "POST":
        password = request.form["current_password"]
        name = request.form["name"]
        new_password = request.form["new_password"]
        confirm_password = request.form["confirm_password"]
        
        if new_password != confirm_password:
            return "<h1>New passwords do not match</h1>"
        
        user = one_student(name)
        if user and check_password_hash(user[5],password):  # Adjust the index if necessary
        # if user :  # Adjust the index if necessary
            update_password(name, new_password)
            return "<h1>Password updated successfully</h1>"
        else:
            return "<h1>Current password is incorrect</h1>"
    
    return render_template("updatw.html")

@app.route("/session_data")
def session_data():
    # if 'username' not in session:
        # return redirect(url_for('login'))
    
    session_items = {key: session[key] for key in session}
    return render_template("session.html", session_items=session_items)

if __name__ == "__main__":
    app.run(debug=True)