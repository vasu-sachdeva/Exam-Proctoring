## Edited By Durvesh

from flask import Flask, render_template, request, redirect, url_for, jsonify, flash,session, redirect
from flask_mysqldb import MySQL
from flask_mail import Mail, Message
import math, random 
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, DateTimeField, BooleanField, IntegerField, DecimalField, HiddenField, SelectField, RadioField
from flask_wtf import FlaskForm
from functools import wraps
from wtforms.fields import DateField, TimeField
from datetime import timedelta, datetime
from wtforms.validators import ValidationError, NumberRange,InputRequired,Length
from flask_wtf.file import FileField, FileRequired, FileAllowed
from coolname import generate_slug
import pandas as pd
from objective import ObjectiveTest	
import numpy as np
import cv2
import json
import base64
# import camera
from deepface import DeepFace

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'quizapp'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'examproject2024@gmail.com'
app.config['MAIL_PASSWORD'] = 'hhcgxhwwmhthepal'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

app.secret_key = 'cvproject'
mysql = MySQL(app)

uid = 123456
email = "abc@abc.com"

suid = 234567
semail = 'cde@cde.com'

name = "Vasu"
email_std = "a@a.com"
sender = 'youremail@abc.com'

def user_role_professor(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if 'logged_in' in session:
			if session['user_role'] == "teacher":
				return f(*args, **kwargs)
			else:
				flash('You dont have privilege to access this page!','danger')
				return render_template("404.html")
		else:
			flash('Unauthorized, Please login!','danger')
			return redirect(url_for('login'))
	return wrap

class UploadForm(FlaskForm):
	subject = StringField('Subject',validators=[InputRequired(message="required")])
	topic = StringField('Topic')
	doc = FileField('CSV Upload', validators=[FileRequired()])
	start_date = DateField('Start Date')
	start_time = TimeField('Start Time', default=datetime.utcnow()+timedelta(hours=5.5))
	end_date = DateField('End Date')
	end_time = TimeField('End Time', default=datetime.utcnow()+timedelta(hours=5.5))
	calc = BooleanField('Enable Calculator')
	neg_mark = DecimalField('Enable negative marking in % ', validators=[NumberRange(min=0, max=100)])
	duration = IntegerField('Duration(in min)')
	password = PasswordField('Exam Password', [Length(min=3, max=6, message="short password")])

	def validate_end_date(form, field):
		if field.data < form.start_date.data:
			raise ValidationError("End date must not be earlier than start date.")
	
	def validate_end_time(form, field):
		start_date_time = datetime.strptime(str(form.start_date.data) + " " + str(form.start_time.data),"%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d %H:%M")
		end_date_time = datetime.strptime(str(form.end_date.data) + " " + str(field.data),"%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d %H:%M")
		if start_date_time >= end_date_time:
			raise ValidationError("End date time must not be earlier/equal than start date time")
	
	def validate_start_date(form, field):
		if datetime.strptime(str(form.start_date.data) + " " + str(form.start_time.data),"%Y-%m-%d %H:%M:%S") < datetime.now():
			raise ValidationError("Start date and time must not be earlier than current")

@app.route("/")
def index():
	return render_template('index.html', messages = 'My name is proctor')

def generateOTP() : 
	digits = "0123456789"
	OTP = "" 
	for i in range(5) : 
		OTP += digits[math.floor(random.random() * 10)] 
	return OTP 

@app.route('/register', methods=['GET','POST'])
def register():
	if request.method == 'POST':
		name = request.form['name']
		email = request.form['email']
		password = request.form['password']
		user_type = request.form['user_type']
		# session['tempName'] = name
		# session['tempEmail'] = email
		# session['tempPassword'] = password
		# session['tempUT'] = user_type
		# sesOTP = generateOTP()
		# session['tempOTP'] = sesOTP
		msg1 = Message('MyProctor.ai - OTP Verification', sender = sender, recipients = [email])
		msg1.body = "New Account opening - Your OTP Verfication code is "+sesOTP+"."
		mail.send(msg1)
		return redirect(url_for('verifyEmail')) 
	return render_template('register.html')


@app.route('/verifyEmail', methods=['GET','POST'])
def verifyEmail():
	if request.method == 'POST':
		theOTP = request.form['eotp']
		# mOTP = session['tempOTP']
		# dbName = session['tempName']
		# dbEmail = session['tempEmail']
		# dbPassword = session['tempPassword']
		# dbUser_type = session['tempUT']
		# dbImgdata = session['tempImage']
		if(theOTP == OTP):
			cur = mysql.connection.cursor()
			ar = cur.execute('INSERT INTO users(name, email, password, user_type, user_image, user_login) values(%s,%s,%s,%s,%s,%s)', (dbName, dbEmail, dbPassword, dbUser_type, dbImgdata,0))
			mysql.connection.commit()
			if ar > 0:
				flash("Thanks for registering! You are sucessfully verified!.")
				return  redirect(url_for('login'))
			else:
				flash("Error Occurred!")
				return  redirect(url_for('login')) 
			cur.close()
			session.clear()
		else:
			return render_template('register.html',error="OTP is incorrect.")
	return render_template('verifyEmail.html')

@app.route('/login', methods=['GET','POST'])
def login():
	if request.method == 'POST':
		email = request.form['email']
		password_candidate = request.form['password']
		user_type = request.form['user_type']
		cur = mysql.connection.cursor()
		results1 = cur.execute('SELECT uid, name, email, password, user_type, user_image from users where email = %s and user_type = %s and user_login = 0' , (email,user_type))
		if results1 > 0:
			cresults = cur.fetchone()
			password = cresults['password']
			name = cresults['name']
			uid = cresults['uid']
		else:
			error = 'Already Login or Email was not found!'
			return render_template('login.html', error=error)
	return render_template('login.html')

@app.route("/professor_index")
def professor_index():
	return render_template('professor_index.html')

@app.route("/student_index")
def student_index():
	return render_template('student_index.html')

@app.route("/create-test", methods = ['GET', 'POST'])
def create_test():
	form = UploadForm()
	if request.method=='POST' and form.validate_on_submit():
		test_id = generate_slug(2)
		# filename = secure_filename(form.doc.data.filename)
		filestream = form.doc.data
		filestream.seek(0)
		ef = pd.read_csv(filestream)
		fields = ['qid','q','a','b','c','d','ans','marks']
		df = pd.DataFrame(ef, columns = fields)
		print(df)
		cur = mysql.connection.cursor()
		for row in df.index:
			cur.execute('INSERT INTO questions(test_id,qid,q,a,b,c,d,ans,marks,uid) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)', (test_id, df['qid'][row], df['q'][row], df['a'][row], df['b'][row], df['c'][row], df['d'][row], df['ans'][row], df['marks'][row], uid))
			cur.connection.commit()
		start_date = form.start_date.data
		end_date = form.end_date.data
		start_time = form.start_time.data
		end_time = form.end_time.data
		start_date_time = str(start_date) + " " + str(start_time)
		end_date_time = str(end_date) + " " + str(end_time)
		neg_mark = int(form.neg_mark.data)
		calc = int(form.calc.data)
		duration = int(form.duration.data)*60
		password = form.password.data
		subject = form.subject.data
		topic = form.topic.data
		# print(form.subject.errors)
		# proctor_type = form.proctor_type.data
		print(start_date, end_date, start_time, end_time, start_date_time, end_date_time, neg_mark, calc, duration, password, subject, topic)
		cur.execute('INSERT INTO teachers (email, test_id, test_type, start, end, duration, show_ans, password, subject, topic, neg_marks, calc, uid) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
			(email, test_id, "objective", start_date_time, end_date_time, duration, 1, password, subject, topic, neg_mark, calc, uid))
		mysql.connection.commit()
		cur.close()
		flash(f'Exam ID: {test_id}', 'success')
		return redirect(url_for('professor_index'))
	return render_template('create_test.html', form = form)

@app.route('/generate_test')
def generate_test():
	return render_template('generate_test.html')

@app.route('/test_generate', methods=["GET", "POST"])
def test_generate():
	if request.method == "POST":
		inputText = request.form["itext"]
		testType = request.form["test_type"]
		noOfQues = request.form["noq"]
		if testType == "objective":
			objective_generator = ObjectiveTest(inputText,noOfQues)
			question_list, answer_list = objective_generator.generate_test()
			testgenerate = zip(question_list, answer_list)
			return render_template('generatedtestdata.html', cresults = testgenerate)
		else:
			return None

@app.route('/viewquestions', methods=['GET'])
# @user_role_professor
def viewquestions():
	cur = mysql.connection.cursor()
	results = cur.execute('SELECT test_id from teachers where email = %s and uid = %s', (email,uid))
	if results > 0:
		cresults = cur.fetchall()
		cur.close()
		return render_template("viewquestions.html", cresults = cresults)
	else:
		return render_template("viewquestions.html", cresults = None)

@app.route('/displayquestions',methods=['POST'])
# @user_role_professor
def displayquestions():
	tid = request.form['choosetid']
	cur = mysql.connection.cursor()
	cur.execute('SELECT * from questions WHERE test_id = %s', (tid,))
	## additional comma to make it tuple for single value tid
	results = cur.fetchall()
	cur.close()
	return render_template("displayquestions.html", callresults = results)

@app.route(f'/disptests', methods=['GET'])
def disptests():
	cur = mysql.connection.cursor()
	res = cur.execute('SELECT test_id,password,subject,topic FROM teachers WHERE uid = %s and email = %s',(uid,email))
	if res>0:
		tests = cur.fetchall()
		cur.close()
		return render_template('disptests.html',tests = tests)
	return render_template('disptests.html',tests = None)


@app.route('/deltidlist', methods=['GET'])
# @user_role_professor
def deltidlist():
	cur = mysql.connection.cursor()
	results = cur.execute('SELECT * from teachers where email = %s and uid = %s', (email,uid))
	print(results)
	if results > 0:
		cresults = cur.fetchall()
		print(cresults)
		now = datetime.now()
		now = now.strftime("%Y-%m-%d %H:%M:%S")
		now = datetime.strptime(now,"%Y-%m-%d %H:%M:%S")
		testids = []
		for a in cresults:
			if datetime.strptime(str(a['start']),"%Y-%m-%d %H:%M:%S") > now:
				testids.append(a['test_id'])
		cur.close()
		return render_template("deltidlist.html", cresults = testids)
	else:
		return render_template("deltidlist.html", cresults = None)


@app.route('/deldispques', methods=['POST'])
# @user_role_professor
def deldispques():
	if request.method == 'POST':
		tidoption = request.form['choosetid']
		cur = mysql.connection.cursor()
		cur.execute('SELECT * from questions where test_id = %s and uid = %s', (tidoption,uid))
		callresults = cur.fetchall()
		cur.close()
		return render_template("deldispques.html", callresults = callresults, tid = tidoption)

@app.route('/delete_questions/<testid>', methods=['POST'])
# @user_role_professor
def delete_questions(testid):
	cur = mysql.connection.cursor()
	msg = '' 
	if request.method == 'POST':
		testqdel = request.json['qids']
		if testqdel:
			if ',' in testqdel:
				testqdel = testqdel.split(',')
				for getid in testqdel:
					cur.execute('DELETE FROM questions WHERE test_id = %s and qid =%s and uid = %s', (testid,getid,uid))
					mysql.connection.commit()
				resp = jsonify('<span style=\'color:green;\'>Questions deleted successfully</span>')
				resp.status_code = 200
				return resp
			else:
				cur.execute('DELETE FROM questions WHERE test_id = %s and qid =%s and uid = %s', (testid,testqdel,uid))
				mysql.connection.commit()
				resp = jsonify('<span style=\'color:green;\'>Questions deleted successfully</span>')
				resp.status_code = 200
				return resp


# @app.route('/viewstudentslogs', methods=['GET'])
# # @user_role_professor
# def viewstudentslogs():
# 	cur = mysql.connection.cursor()
# 	results = cur.execute('SELECT test_id from teachers where email = %s and uid = %s and proctoring_type = 0', (email,uid))
# 	if results > 0:
# 		cresults = cur.fetchall()
# 		cur.close()
# 		return render_template("viewstudentslogs.html", cresults = cresults)
# 	else:
# 		return render_template("viewstudentslogs.html", cresults = None)


@app.route('/<testid>/<qid>')
# @user_role_professor
def del_qid(testid, qid):
	cur = mysql.connection.cursor()
	results = cur.execute('DELETE FROM questions where test_id = %s and qid = %s and uid = %s', (testid,qid,uid))
	mysql.connection.commit()
	if results>0:
		msg="Deleted successfully"
		flash('Deleted successfully.', 'success')
		cur.close()
		return render_template("deldispques.html", success=msg)
	else:
		return render_template('deldispques.html')

################### UPDATE QUESTIONS ######################

@app.route('/updatetidlist', methods=['GET'])
# @user_role_professor
def updatetidlist():
	cur = mysql.connection.cursor()
	results = cur.execute('SELECT * from teachers where email = %s and uid = %s', (email,uid))
	if results > 0:
		cresults = cur.fetchall()
		now = datetime.now()
		now = now.strftime("%Y-%m-%d %H:%M:%S")
		now = datetime.strptime(now,"%Y-%m-%d %H:%M:%S")
		testids = []
		for a in cresults:
			if datetime.strptime(str(a['start']),"%Y-%m-%d %H:%M:%S") > now:
				testids.append(a['test_id'])
		cur.close()
		return render_template("updatetidlist.html", cresults = testids)
	else:
		return render_template("updatetidlist.html", cresults = None)

@app.route('/updatedispques', methods=['GET','POST'])
# @user_role_professor
def updatedispques():
	if request.method == 'POST':
		tidoption = request.form['choosetid']
		# et = examtypecheck(tidoption)
		cur = mysql.connection.cursor()
		cur.execute('SELECT * from questions where test_id = %s and uid = %s', (tidoption,uid))
		callresults = cur.fetchall()
		cur.close()
		return render_template("updatedispques.html", callresults = callresults)

@app.route('/update/<testid>/<qid>', methods=['GET','POST'])
# @user_role_professor
def update_quiz(testid, qid):
	if request.method == 'GET':
		cur = mysql.connection.cursor()
		cur.execute('SELECT * FROM questions where test_id = %s and qid =%s and uid = %s', (testid,qid,uid))
		uresults = cur.fetchall()
		mysql.connection.commit()
		return render_template("updateQuestions.html", uresults=uresults)
	if request.method == 'POST':
		ques = request.form['ques']
		ao = request.form['ao']
		bo = request.form['bo']
		co = request.form['co']
		do = request.form['do']
		anso = request.form['anso']
		markso = request.form['mko']
		cur = mysql.connection.cursor()
		cur.execute('UPDATE questions SET q = %s, a = %s, b = %s, c = %s, d = %s, ans = %s, marks = %s where test_id = %s and qid = %s and uid = %s', (ques,ao,bo,co,do,anso,markso,testid,qid,uid))
		cur.connection.commit()
		flash('Updated successfully.', 'success')
		cur.close()
		return redirect(url_for('updatetidlist'))
	else:
		flash('ERROR  OCCURED.', 'error')
		return redirect(url_for('updatetidlist'))

###################################### Student DashBoard ##########################################

class TestForm(Form):
	test_id = StringField('Exam ID')
	password = PasswordField('Exam Password')
	img_hidden_form = HiddenField(label=(''))

############ take/give Exam #################
@app.route('/<email>/tests-given', methods = ['POST','GET'])
#@user_role_student
def tests_given(email):
	if request.method == "GET":
		# if email == session['email']:
		cur = mysql.connection.cursor()
		resultsTestids = cur.execute('select studenttestinfo.test_id as test_id from studenttestinfo,teachers where studenttestinfo.email = %s and studenttestinfo.uid = %s and studenttestinfo.completed=1 and teachers.test_id = studenttestinfo.test_id and teachers.show_ans = 1 ', (email, uid))
		resultsTestids = cur.fetchall()
		cur.close()
		return render_template('tests_given.html', cresults = resultsTestids)
		# else:
		# 		flash('You are not authorized', 'danger')
		# 	return redirect(url_for('student_index'))
	elif request.method == "POST":
		tidoption = request.form['choosetid']
		cur = mysql.connection.cursor()
		cur.execute('SELECT test_type from teachers where test_id = %s',[tidoption])
		callresults = cur.fetchone()
		cur.close()
		# if callresults['test_type'] == "objective":
		cur = mysql.connection.cursor()
		results = cur.execute('select distinct(students.test_id) as test_id, students.email as email, subject,topic,neg_marks from students,studenttestinfo,teachers where students.email = %s and teachers.test_type = %s and students.test_id = %s and students.test_id=teachers.test_id and students.test_id=studenttestinfo.test_id and studenttestinfo.completed=1', (email, "objective", tidoption))
		results = cur.fetchall()
		cur.close()
		results1 = []
		studentResults = None
		for a in results:
			results1.append(neg_marks(a['email'],a['test_id'],a['neg_marks']))
			studentResults = zip(results,results1)
		return render_template('obj_result_student.html', tests=studentResults)

@app.route('/<email_id>/student_test_history')
def student_test_history(email_id):
	if email_id == email_std:
		cur = mysql.connection.cursor()
		results = cur.execute('SELECT a.test_id, b.subject, b.topic \
			from studenttestinfo a, teachers b where a.test_id = b.test_id and a.email=%s  \
			and a.completed=1', [email_id])
		results = cur.fetchall()
		return render_template('student_test_history.html', tests=results)
	else:
		flash('You are not authorized', 'danger')
		return redirect(url_for('student_index'))

def neg_marks(email,testid,negm):
	cur=mysql.connection.cursor()
	results = cur.execute("SELECT q.marks, q.qid AS qid, q.ans AS correct, IFNULL(s.ans, 0) AS marked FROM questions q INNER JOIN students s ON s.test_id = q.test_id AND s.test_id = %s AND s.email = %s AND s.qid = q.qid GROUP BY q.marks, q.qid, q.ans, s.ans ORDER BY q.qid ASC", (testid, email))
	data=cur.fetchall()

@app.route("/give-test", methods = ['GET', 'POST'])
# @user_role_student
def give_test():
	global duration, marked_ans, calc, subject, topic, proctortype
	form = TestForm(request.form)
	if request.method == 'POST' and form.validate():
		test_id = form.test_id.data
		password_candidate = form.password.data
		# imgdata1 = form.image_hidden_form.data
		cur1 = mysql.connection.cursor()
		results1 = cur1.execute('SELECT user_image from users where email = %s and user_type = %s ', ('cde@cde.com','student'))
		if results1 > 0:
			cresults = cur1.fetchone()
			imgdata2 = cresults['user_image']
			cur1.close()
			# nparr1 = np.frombuffer(base64.b64decode(imgdata2), np.uint8)
			# nparr2 = np.frombuffer(base64.b64decode(imgdata2), np.uint8)
			# image1 = cv2.imdecode(nparr1, cv2.COLOR_BGR2GRAY)
			# image2 = cv2.imdecode(nparr2, cv2.COLOR_BGR2GRAY)
			# img_result  = DeepFace.verify(image1, image2, enforce_detection = False)
			# print(img_result)
			# if img_result["verified"] == True:
			img_result = True
			if img_result == True:
				cur = mysql.connection.cursor()
				results = cur.execute('SELECT * from teachers where test_id = %s', [test_id])
				if results > 0:
					data = cur.fetchone()
					password = data['password']
					duration = data['duration']
					calc = data['calc']
					subject = data['subject']
					topic = data['topic']
					start = data['start']
					start = str(start)
					end = data['end']
					end = str(end)
					proctortype = data['proctoring_type']
					if password == password_candidate:
						now = datetime.now()
						now = now.strftime("%Y-%m-%d %H:%M:%S")
						now = datetime.strptime(now,"%Y-%m-%d %H:%M:%S")
						if datetime.strptime(start,"%Y-%m-%d %H:%M:%S") < now and datetime.strptime(end,"%Y-%m-%d %H:%M:%S") > now:
							results = cur.execute('SELECT time_to_sec(time_left) as time_left,completed from studentTestInfo where email = %s and test_id = %s', ('cde@cde.com', test_id))
							if results > 0:
								results = cur.fetchone()
								# print(results)
								is_completed = results['completed']
								if is_completed == 0:
									time_left = results['time_left']
									if time_left <= duration:
										duration = time_left
										results = cur.execute('SELECT qid , ans from students where email = %s and test_id = %s and uid = %s', ('cde@cde.com', test_id, 234567))
										marked_ans = {}
										if results > 0:
											results = cur.fetchall()
											for row in results:
												print(row['qid'])
												qiddb = ""+row['qid']
												print(qiddb)
												print(type(marked_ans))
												marked_ans[qiddb] = row['ans']
											marked_ans = json.dumps(marked_ans)
								else:
									flash('Exam already given', 'success')
									return redirect(url_for('give_test'))
							else:
								cur.execute('INSERT into studentTestInfo (email, test_id,time_left,uid) values(%s,%s,SEC_TO_TIME(%s),%s)', ('cde@cde.com', test_id, duration, 234567))
								mysql.connection.commit()
								results = cur.execute('SELECT time_to_sec(time_left) as time_left,completed from studentTestInfo where email = %s and test_id = %s and uid = %s', ('cde@cde.com', test_id, 234567))
								if results > 0:
									results = cur.fetchone()
									is_completed = results['completed']
									if is_completed == 0:
										time_left = results['time_left']
										if time_left <= duration:
											duration = time_left
											results = cur.execute('SELECT * from students where email = %s and test_id = %s and uid = %s', ('cde@cde.com', test_id, 234567))
											marked_ans = {}
											if results > 0:
												results = cur.fetchall()
												for row in results:
													marked_ans[row['qid']] = row['ans']
												marked_ans = json.dumps(marked_ans)
						else:
							if datetime.strptime(start,"%Y-%m-%d %H:%M:%S") > now:
								flash(f'Exam start time is {start}', 'danger')
							else:
								flash(f'Exam has ended', 'danger')
							return redirect(url_for('give_test'))
						return redirect(url_for('test' , testid = test_id))
					else:
						flash('Invalid password', 'danger')
						return redirect(url_for('give_test'))
				flash('Invalid testid', 'danger')
				cur.close()
				return redirect(url_for('give_test'))
			else:
				flash('Image not Verified', 'danger')
				return redirect(url_for('give_test'))
	return render_template('give_test.html', form = form)

@app.route('/give-test/<testid>', methods=['GET','POST'])
# @user_role_student
def test(testid):
	global duration, marked_ans, calc, subject, topic, proctortype
	if request.method == 'GET':
		data = {'duration': duration, 'marks': '', 'q': '', 'a': '', 'b':'','c':'','d':'' }
		# print("hi")
		# return render_template('testquiz.html' ,**data, answers=marked_ans, calc=calc, subject=subject, topic=topic, tid=testid, proctortype=proctortype)
		try:
			data = {'duration': duration, 'marks': '', 'q': '', 'a': '', 'b':'','c':'','d':'' }
			# print("hi")
			return render_template('testquiz.html' ,**data, answers=marked_ans, calc=calc, subject=subject, topic=topic, tid=testid, proctortype=proctortype)
		except:
			return redirect(url_for('give_test'))
	else:
		cur = mysql.connection.cursor()
		flag = request.form['flag']
		if flag == 'get':
			num = request.form['no']
			results = cur.execute('SELECT test_id,qid,q,a,b,c,d,ans,marks from questions where test_id = %s and qid =%s',(testid, num))
			if results > 0:
				data = cur.fetchone()
				del data['ans']
				cur.close()
				return json.dumps(data)
		elif flag=='mark':
			qid = request.form['qid']
			ans = request.form['ans']
			cur = mysql.connection.cursor()
			results = cur.execute('SELECT * from students where test_id =%s and qid = %s and email = %s', (testid, qid, semail))
			if results > 0:
				cur.execute('UPDATE students set ans = %s where test_id = %s and qid = %s and email = %s', (testid, qid, semail))
				mysql.connection.commit()
				cur.close()
			else:
				cur.execute('INSERT INTO students(email,test_id,qid,ans,uid) values(%s,%s,%s,%s,%s)', (semail, testid, qid, ans, suid))
				mysql.connection.commit()
				cur.close()
		elif flag=='time':
			cur = mysql.connection.cursor()
			time_left = request.form['time']
			try:
				cur.execute('UPDATE studentTestInfo set time_left=SEC_TO_TIME(%s) where test_id = %s and email = %s and uid = %s and completed=0', (time_left, testid, semail, suid))
				mysql.connection.commit()
				cur.close()
				return json.dumps({'time':'fired'})
			except:
				pass
		else:
			cur = mysql.connection.cursor()
			cur.execute('UPDATE studentTestInfo set completed=1,time_left=sec_to_time(0) where test_id = %s and email = %s and uid = %s', (testid, semail,suid))
			mysql.connection.commit()
			cur.close()
			flash("Exam submitted successfully", 'info')
			return json.dumps({'sql':'fired'})

@app.route('/randomize', methods = ['POST'])
def random_gen():
	if request.method == "POST":
		id = request.form['id']
		cur = mysql.connection.cursor()
		results = cur.execute('SELECT count(*) from questions where test_id = %s', [id])
		if results > 0:
			data = cur.fetchone()
			total = data['count(*)']
			nos = list(range(1,int(total)+1))
			random.Random(id).shuffle(nos)
			cur.close()
			return json.dumps(nos)


# PROCTORING

@app.route('/viewstudentslogs', methods=['GET'])
# @user_role_professor
def viewstudentslogs():
	cur = mysql.connection.cursor()
	results = cur.execute('SELECT test_id from teachers where email = %s and uid = %s and proctoring_type = 0', (email, uid))
	if results > 0:
		cresults = cur.fetchall()
		cur.close()
		return render_template("viewstudentslogs.html", cresults = cresults)
	else:
		return render_template("viewstudentslogs.html", cresults = None)

@app.route('/displaystudentsdetails', methods=['GET','POST'])
# @user_role_professor
def displaystudentsdetails():
	if request.method == 'POST':
		tidoption = request.form['choosetid']
		cur = mysql.connection.cursor()
		cur.execute('SELECT DISTINCT email,test_id from proctoring_log where test_id = %s', [tidoption])
		callresults = cur.fetchall()
		cur.close()
		return render_template("displaystudentsdetails.html", callresults = callresults)

if __name__ == "__main__":
	app.run()

# updated by vasu on 17/5 9:55am
