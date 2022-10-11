import os.path
import pymysql
from flask import url_for, request, redirect, render_template, send_from_directory
from . import app, db

pymysql.install_as_MySQLdb()

def make_connection_to_db():
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password="root",
        db='training',
    )
    return conn, conn.cursor()


@app.route("/setup")
def setup():
    db.create_all()
    return "setup"


@app.route("/", methods=['GET', 'POST'])
def home_page():
    if request.method == 'POST':
        url = url_for('offer')
        return redirect(url)
    else:
        return render_template('home_page.html')


@app.route("/offer", methods=['GET', 'POST'])
def offer():
    message = ''
    username = ''

    if request.method == 'POST':
        username = request.form.get('username')
        phone = request.form.get('phone')
        email = request.form.get('email')
        url = url_for('get_offer_page')

        conn, cur = make_connection_to_db()

        attrs = {
            "id": '0',
            "name": str(username),
            "phone": str(phone),
            "email": str(email),
        }

        cur.execute(
            f"INSERT INTO `offers` (%s,%s,%s,%s) VALUES (%s,'%s',%s,'%s')" \
               % tuple(list(attrs.keys()) + list(attrs.values())))
        #print(cur.fetchall())

        conn.commit()
        conn.close()

        return redirect(url)
    else:
        return render_template('offer_page.html', message=message)

@app.route("/get_offer", methods=['GET', 'POST'])
def get_offer_page():
        return render_template('get_offer_page.html')

@app.route("/login", methods=['GET', 'POST'])
def log_in():
    message = ''
    username = ''
    password = ''

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

    if username == 'root' and password == 'root':
        message = "Correct username and password"
        url = url_for('admin')
        return redirect(url)
    else:
        message = "Wrong username or password"
        return render_template('login_page.html', message=message)


@app.route("/download_resume")
def download_resume():
    filepath = os.path.abspath('MyResumeURL.pdf')
    return send_from_directory(directory=os.path.dirname(filepath), path='MyResumeURL.pdf')

@app.route("/admin")
def admin():
    conn, cur = make_connection_to_db()

    cur.execute("SELECT * FROM `offers`")
    offers = cur.fetchall()
    #print(offers)

    conn.commit()
    conn.close()
    return render_template('admin_page.html', offers = offers)

app.run()


#TODO add css
