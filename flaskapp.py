import sqlite3
from flask import Flask, request, g, render_template, redirect, url_for, session, flash, send_file

app = Flask(__name__)

app.secret_key = 'not_a_secret'

DATABASE = '/home/ubuntu/flaskapp/users.db'

def connect_to_database():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users 
                  (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, password TEXT, firstname TEXT,
                   lastname TEXT, email TEXT)''')
    conn.commit()
    return conn

@app.route('/')
def index():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    email = request.form['email']
    try:
        with sqlite3.connect(DATABASE) as conn:
            c = conn.cursor()
            c.execute("INSERT INTO users (username, password, firstname, lastname, email) VALUES (?, ?, ?, ?, ?)",
                      (username, password, firstname, lastname, email))
            conn.commit()
            flash('Registration successful!', 'success')
            return redirect(url_for('get_user', username=username))
    except sqlite3.IntegrityError:
        flash('Username already taken, please choose another', 'error')
        return redirect(url_for('index'))
    except Exception as e:  # Catch any other exceptions
        flash('An error occurred: {}'.format(str(e)), 'error')
        return redirect(url_for('index'))

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    user = execute_query("SELECT * FROM users WHERE username = ? AND password = ?", [username, password])
    if user:
        session['username'] = username
        flash('You have successfully logged in!', 'success')
        return redirect(url_for('get_user', username=username))
    else:
        error = 'Invalid username or password'
        return render_template('register.html', error=error)

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have successfully logged out!', 'info')
    return redirect(url_for('index'))

#Used to display wordcount in get_user
def wordcount(fileaddress):
    count = 0
    with open(fileaddress,'r') as file:
        data = file.read()
        lines = data.split()
        count += len(lines)
    return(count)


@app.route("/user/<username>")
def get_user(username):
    rows = execute_query("""SELECT * FROM users WHERE username = ?""", [username])
    count = wordcount('/home/ubuntu/flaskapp/limerick-1.txt') # extra credit limerick
    if rows:
        return render_template('profile.html', user=rows[0],wordcount=count)
    return "User not found"

@app.route("/download/<filename>")
def get_file(filename):
    try:
        return(send_file("/home/ubuntu/flaskapp/" + str(filename), as_attachment = True))
        return(file)
    except Exception as e:
        return  f"Error: {str(e)}"



def get_db():
    if 'db' not in g:
        g.db = connect_to_database()
    return g.db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

def execute_query(query, args=()):
    cur = get_db().execute(query, args)
    rows = cur.fetchall()
    cur.close()
    return rows

@app.route("/viewdb")
def viewdb():
    rows = execute_query("""SELECT * FROM users""")
    return '<br>'.join(str(row) for row in rows)

if __name__ == '__main__':
    app.run(debug=True)
