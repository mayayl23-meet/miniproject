from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'gro239u01hpii12iepop91023md'

# home page route:
@app.route('/', methods=['GET', 'POST'])
def home():
	return render_template("home.html")



# about page route:
@app.route('/about', methods=['GET', 'POST'])
def about():
	return render_template("about.html")



# login page route
@app.route('/login', methods=['GET', 'POST'])
def login():
	error = ""
	if request.method == 'POST':
	   username = request.form['username']
	   password = request.form['password']
	   try:
	   	login_session['user'] = auth.sign_in_with_email_and_password(email, password)
	   	return redirect(url_for('home'))
	   except:
	   	error = "Authentication failed"
	return render_template("login.html")



# signup page route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
	error = ""
	if request.method == 'POST':
		email = request.form['email']
		password = request.form['password']
		username = request.form['username']
		age = request.form['age']
		try:
			login_session['user'] = auth.create_user_with_email_and_password(email, password)
			user = {'username': request.form['username'], 'email': request.form['email'], 'password': request.form['password'], 'age': request.form['age']}
			db.child("Users").child(login_session['user']['localId']).set(user)
			return redirect(url_for('home'))


		except:
		   error = "Authentication failed"
	return render_template("signup.html")


# sign out page route
@app.route('/signout', methods=['GET', 'POST'])
def signout():
	login_session['user'] = None
	auth.current_user = None
	return redirect(url_for('login'))


# all posts route:
@app.route('/all_uploads', methods=['GET', 'POST'])
def all_uploads():
	return render_template("all_uploads.html")



@app.route('/post1', methods=['GET', 'POST'])
def post1():
	return render_template("post1.html")	

@app.route('/comments', methods=['GET', 'POST'])
def comments():
    if request.method == 'POST':
        Title = request.form['title']
        Text = request.form['text']
        comment = {'Title': request.form['title'], 'Text': request.form['text'], "uid": login_session['user']['localId']}
        db.child("Comments").push(comment)
        return redirect(url_for('all_comments'))
        # try:# except:
        #     error = "Authetication Failed"
        #     print(error)
    return render_template("comments.html")


@app.route('/all_comments', methods=['GET', 'POST'])
def all_comments():
        all_comments = db.child("Comments").get().val()
        return render_template('all_comments.html', comment=all_comments)


# @app.route('/delete', methods=['GET', 'POST'])
# def delete():
# 	if request.method == 'GET':
# 		try:
# 			db.child("Users").child(login_session['user']['localId']).remove()
# 			return redirect(url_for('all_comments'))
# 		except:
# 			error = "Couldn’t delete comment"






config = {
  'apiKey': "AIzaSyC0XynHrhskclzWQ7Db-7PyB_rRs5fURWs",
  'authDomain': "maya-s-blog.firebaseapp.com",
  'projectId': "maya-s-blog",
  'storageBucket': "maya-s-blog.appspot.com",
  'messagingSenderId': "843551918339",
  'appId': "1:843551918339:web:f4f8e15d6cf723f0e18136",
  'measurementId': "G-V76G1SD951",
  'databaseURL': "https://maya-s-blog-default-rtdb.europe-west1.firebasedatabase.app/"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()



if __name__ == '__main__':
	app.run(debug = True)