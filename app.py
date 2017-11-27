import os,sys
import json
from flask import Flask, render_template, flash, redirect, url_for, session, request, logging, jsonify
from werkzeug import secure_filename
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, DateField, SelectField, SelectMultipleField, widgets
from passlib.hash import sha256_crypt
from functools import wraps
from flask_jsglue import JSGlue
from flask import send_from_directory
from collections import defaultdict



#GLOBALS
UPLOAD_FOLDER = '/home/wjeo001/py/static/quick-quiz-master/img'
UPLOAD_FOLDER_QUIZ = '/home/wjeo001/py/static/quick-quiz-master/quiz_lib'
ALLOWED_EXTENSIONS = set(['json', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


app = Flask(__name__)

# @app.template_filter()
# def datetimefilter(value, format='%d/%m/%Y'):
#     """convert a datetime to a different format."""
#     return value.strftime(format)

# app.jinja_env.filters['datetimefilter'] = datetimefilter

# app.config["DEBUG"] = True
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

APP_ROOT=os.path.dirname(os.path.abspath(__file__))

# config MySql
# app.config['MYSQL_HOST']='wjeo001.mysql.pythonanywhere-services.com'
# app.config['MYSQL_USER']='wjeo001'
# app.config['MYSQL_PASSWORD']='mar_Vjdls!2'
# app.config['MYSQL_DB']='wjeo001$gen_001'
# app.config['MYSQL_CURSORCLASS']='DictCursor'
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='mar_Vjdls!2'
app.config['MYSQL_DB']='gen_001'
app.config['MYSQL_CURSORCLASS']='DictCursor'

# init MYSQL
mysql=MySQL(app)

#init JSGlue
jsglue = JSGlue(app)


#Articles = Articles();

@app.route('/text')
def text():
	return render_template('text.html')

@app.route('/')
#index
def index():
	return home()
	#return render_template('home.html')
#home
@app.route('/home')
def home():
	#create cursor
	cur=mysql.connection.cursor()

	#get articles
	s="select * from articles order by id desc limit 5"
	result=cur.execute(s)
	articles=cur.fetchall()



	#close connection
	cur.close()

	return render_template('home.html', articles=articles)


#about
@app.route('/about')
def about():
	return render_template('about.html')

#Articles
@app.route('/articles')
def articles():
	#create cursor
	cur=mysql.connection.cursor()

	#get articles
	result=cur.execute("select * from articles")

	articles=cur.fetchall()
	if result > 0:
		return render_template('articles.html', articles=articles)
	else:
		msg='No articles found'
		return render_template('articles.html', msg=msg)

	#close connection
	cur.close()

#single article
@app.route('/article/<string:id>/')
def article(id):
	#create cursor
	cur=mysql.connection.cursor()

	#get article
	result=cur.execute("select * from articles where id =  %s", [id])

	article=cur.fetchone()
	return render_template('article.html', article=article)

#Register form class
class RegisterForm(Form):
	firstname = StringField('FirstName', [validators.Length(min=1, max=50)])
	lastname = StringField('LastName', [validators.Length(min=1, max=50)])
	username = StringField('Username',[validators.Length(min=4, max=25)])
	email = StringField('Email',[validators.Length(min=6,max=50)])
	password = PasswordField('Password', [
			validators.DataRequired(),
			validators.EqualTo('confirm', message='Your record cannot be found')
		])
	confirm = PasswordField('Confirm Password')

#User Register
@app.route('/register', methods=['GET','POST'])
def register():
	form = RegisterForm(request.form)
	if request.method == 'POST' and form.validate():
		firstname = form.firstname.data
		lastname = form.lastname.data
		email = form.email.data
		username = form.username.data
		password = sha256_crypt.encrypt(str(form.password.data))

		#Create cursor
		cur = mysql.connection.cursor()

		#execute
		s="select username from users where username='"+username+"'"
		result=cur.execute(s)
		app.logger.info(result)
		if result>0:
			app.logger.info('duplicate username')
			flash("Username "+ username + " already exists. Please try another username", 'danger')
			cur.close()
			return render_template('Register.html',form=form)
		else:
			s="insert into users(firstname, lastname, email, username, password,power_level) values ('"+firstname+"','"+lastname+"','"+email+"','"+username+"','"+password+"','student')"
			cur.execute(s)
			s="insert into people(firstname, lastname, email, username, people_type) values ('"+firstname+"','"+lastname+"','"+email+"','"+username+"','student')"
			cur.execute(s)

		# Commit to DB
		mysql.connection.commit()

		#close connection
		cur.close()

		flash('You are now registered and can log in', 'success')

		return redirect(url_for('login'))
	return render_template('Register.html', form = form)

#user login
@app.route('/login', methods=['GET','POST'])
def login():
	if request.method == 'POST':
		#get form fields
		username=request.form['username']
		password_candidate=request.form['password']

		#create cursor
		cur=mysql.connection.cursor()

		#get user by username
		s=("select u.username,u.power_level,u.firstname,u.lastname,p.id,u.password "+
			"from users u " +
			"inner join people p on p.username=u.username where u.username='"+username+"'")
		# result=cur.execute("select * from users where username= %s", [username])
		result=cur.execute(s)



		if result > 0:
			# Get stored hash
			data = cur.fetchone()
			password=data['password']

			#compare passwords
			if sha256_crypt.verify(password_candidate,password):
				#app.logger.info('PASSWORD MATCHED')
				session['logged_in'] = True
				session['username']=username
				session['rights']= data['power_level']
				session['fullname']= data['firstname'] + ' ' + data['lastname']
				session['id']=data['id']
				flash('You are now logged in', 'success')
				return redirect(url_for('dashboard'))
			else:
				error='Invalid login'
				return render_template('login.html', error=error)
			#close connection
			cur.close()
		else:
			error='Username not found'
			return render_template('login.html', error=error)



	return render_template('login.html')

#check if user logged in
def is_logged_in(f):
	@wraps(f)
	def wrap(*args,**kwargs):
		if 'logged_in' in session:
			return f(*args, **kwargs)
		else:
			flash('Unauthorised, Please login', 'danger')
			return redirect(url_for('login'))
	return wrap

#check if the user has admin rights
def is_admin(f):
	@wraps(f)
	def wrap(*args,**kwargs):
		a=session['rights']
		if a=='admin':
			return f(*args,**kwargs)
		else:
			flash('You do not have admin rights', 'danger')
			return redirect(url_for('home'))
	return wrap

#Logout
@app.route('/logout')
@is_logged_in
def logout():
	session.clear()
	flash('You are now logged out', 'success')
	return redirect(url_for('login'))

#password reset
@app.route('/resetpw/<string:id>', methods=['GET','POST'])
@is_admin
def resetpw(id):
	cur=mysql.connection.cursor()
	new_pw_string="pw123456"
	newpw=sha256_crypt.encrypt(new_pw_string)
	s="update users set password='{}' where username='{}'".format(newpw,id)
	app.logger.info(s)
	result=cur.execute(s)
	cur.close
	flash("Password reset done","success")
	return redirect(url_for('users'))


#user profile
class ProfileForm(Form):
	firstname=StringField('First Name')
	lastname=StringField('Last Name')
	email=StringField('Email')
	mob=StringField('Mobile Phone')
	dob=DateField('Date of Birth',format='%Y-%m-%d')
	phone=StringField('Phone Number')
	adr_street=StringField('Street Address')
	adr_suburb=StringField('Suburb')
	adr_state=SelectField('State',choices=[('NSW','NSW'),('QLD','QLD'),('VIC','VIC'),('ACT','ACT'),('WA','WA'),('SA','SA'),('NT','NT')])
	adr_postcode=StringField('Postcode')
	adr_type=SelectField('Address Type',choices=[('HOME','HOME'),('POST','POST')])
	# people_type=SelectField('User type',choices=[('student','student'),('staff','staff'),('admin','admin')]) #admin only
	username=StringField('User Name') #admin only

@is_logged_in
@app.route('/profile')
def profile():
	cur = mysql.connection.cursor()
	s="select p.*,a.street_address,a.suburb,a.state,a.postcode,a.addr_type from people p left join address a on a.people_id=people_id where p.username='"+session['username']+"'"
	result=cur.execute(s)
	user=cur.fetchone()
	cur.close()
	return render_template('profile_view.html',user=user)

@is_logged_in
@app.route('/profile_edit/<string:username>',methods=['GET','POST'])
def profile_edit(username):
	form=ProfileForm(request.form)
	cur=mysql.connection.cursor()
	#s="select p.*,a.street_address,a.suburb,a.state,a.postcode,a.addr_type from people p left join address a on a.people_id=people_id where p.username='"+session['username']+"'"
	s="select p.*,a.street_address,a.suburb,a.state,a.postcode,a.addr_type from people p left join address a on a.people_id=p.id where p.username='"+username+"'"
	result=cur.execute(s)
	user=cur.fetchone()
	cur.close()

	form.firstname.data=user['firstname']
	form.lastname.data=user['lastname']
	form.email.data=user['email']
	form.mob.data=user['mob']
	form.dob.data=user['date_of_birth']
	form.phone.data=user['phone']
	form.adr_street.data=user['street_address']
	form.adr_suburb.data=user['suburb']
	form.adr_state.data=user['state']
	form.adr_postcode.data=user['postcode']
	form.adr_type.data=user['addr_type']
	# form.people_type.data=user['people_type']

	if request.method=='POST':
		firstname=request.form['firstname']
		lastname=request.form['lastname']
		email=request.form['email']
		mob=request.form['mob']
		dob=request.form['dob']
		phone=request.form['phone']
		adr_street=request.form['adr_street']
		adr_suburb=request.form['adr_suburb']
		adr_state=request.form['adr_state']
		adr_postcode=request.form['adr_postcode']
		adr_type=request.form['adr_type']
		# people_type=request.form['people_type']

		cur=mysql.connection.cursor()
		#s="update people set firstname='{}', lastname='{}', email='{}', mob='{}', date_of_birth='{}', phone='{}', people_type='{}' where id={}".format(firstname,lastname,email,mob,dob,phone,people_type,session['id'])
		s="update people set firstname='{}', lastname='{}', email='{}', mob='{}', date_of_birth='{}', phone='{}', people_type='student' where username='{}'".format(firstname,lastname,email,mob,dob,phone,username)
		app.logger.info(s)
		#ss=(s+" where id={}").format(session['id'])
		result=cur.execute(s)

		# if 'student' not in request.form['people_type']:
		# 	s="update users set power_level='"+people_type+"' where username='"+username+"'"
		# 	app.logger.info(s)
		# 	result=cur.execute(s)

		#ss="update address set street_address='{}', addr_type='{}', suburb='{}', state='{}', postcode='{}' where people_id={}".format(adr_street,adr_type,adr_suburb,adr_state,adr_postcode,session['id'])
		ss="update address set street_address='{}', addr_type='{}', suburb='{}', state='{}', postcode='{}' where people_id={}".format(adr_street,adr_type,adr_suburb,adr_state,adr_postcode,user['id'])
		app.logger.info(ss)
		result=cur.execute(ss)
		if result<1:
			# ss="insert into address(street_address,addr_type,suburb,state,postcode,people_id) values ('{}','{}','{}','{}','{}',{})".format(adr_street,adr_type,adr_suburb,adr_state,adr_postcode,session['id'])
			ss="insert into address(street_address,addr_type,suburb,state,postcode,people_id) values ('{}','{}','{}','{}','{}',{})".format(adr_street,adr_type,adr_suburb,adr_state,adr_postcode,user['id'])
			app.logger.info(ss)
			result=cur.execute(ss)

		mysql.connection.commit()

		cur.close()
		flash('Profile updated','success')
		if session['id']==user['id']:
			return redirect(url_for('profile'))
		else:
			return redirect(url_for('users'))

	return render_template('profile_edit.html',form=form)

@app.route('/data/dashboard/<string:idx>')
def charttest(idx):
	cur=mysql.connection.cursor()
	s="select c.id, c.course_name, c.course_desc, c.start_date, c.end_date, count(pu.unit_id) as unitcount from people p inner join people_units pu on pu.people_id=p.id inner join courses c on c.id=pu.course_id inner join users on users.username=p.username where pu.status='Active' and users.username='"+session['username']+"' group by c.id, c.course_name, c.course_desc, c.start_date, c.end_date"
	app.logger.info([idx])
	if idx=='2':
		s="select sbj.name, count(un.id) as unitcount from units un inner join people_units pu on pu.unit_id=un.id " \
	      + "inner join people p on p.id=pu.people_id inner join users u on u.username=p.username " \
		  + "left join ref_subjects sbj on sbj.id=un.subject where pu.status='Active' and u.username='" + session['username'] + "' group by sbj.name "

    #This not done yet
    # 	elif idx=='3':
    # 	    s="select qs_name"


	result=cur.execute(s)
	data=cur.fetchall()
	jsn=jsonify(data)
	cur.close()
	return jsn

#Dashboard
@app.route('/dashboard')
@is_logged_in
def dashboard():
	#create cursor
	cur=mysql.connection.cursor()
	#get Enrolled Courses
	s="select c.id, c.course_name, c.course_desc, c.start_date, c.end_date, count(pu.unit_id) as unitcount from people p inner join people_units pu on pu.people_id=p.id inner join courses c on c.id=pu.course_id inner join users on users.username=p.username where pu.status='Active' and users.username='"+session['username']+"' group by c.id, c.course_name, c.course_desc, c.start_date, c.end_date"
	result=cur.execute(s)
	courses=cur.fetchall()
	units=0
	msg=""
	if result < 1:
	 	msg="You don't have any enrolled courses yet"
	else:
		#get Units of the courses for the user
		s="select pu.unit_id,pu.course_id, u.subject, u.unit_name, u.unit_desc, u.start_date,u.end_date,u.semester from people_units pu inner join units u on u.id=pu.unit_id inner join people p on p.id=pu.people_id inner join users on users.username=p.username where users.username='" + session['username']+"'"
		result=cur.execute(s)
		units=cur.fetchall()
	s="select u.unit_name,qs.qs_name,count(pql.qr_id) as attempts from people_unit_quiz_link pql inner join quiz_sets qs on qs.qs_id=pql.qs_id inner join units u on u.id=qs.unit_id where exists (select 1 from people_units pu inner join people p on pu.people_id=p.id where pu_id=pql.pu_id and p.id={}) group by u.unit_name,qs.qs_name".format(session['id'])
	result=cur.execute(s)
	progress=cur.fetchall()
	cur.close()
	return render_template('dashboard.html', msg=msg,courses=courses,units=units, jscourse=jsonify(courses), progress=progress)

#Article form class
class ArticleForm(Form):
	title = StringField('Title', [validators.Length(min=1, max=200)])
	body  = TextAreaField('Body',[validators.Length(min=30)])

#Add Article
@app.route('/add_article',methods=['GET','POST'])
@is_logged_in
def add_article():
	form = ArticleForm(request.form)
	if request.method == 'POST' and form.validate():
		title=form.title.data
		body=form.body.data

		#Create cursor
		cur=mysql.connection.cursor()

		#Execute
		s="select concat(firstname,' ',LastName) as auth from users where username='" + session['username'] + "'"
		result=cur.execute(s)
		authorname=cur.fetchone()

		#cur.execute("insert into articles (title,body,author) values (%s,%s,%s)", (title,body,session['username']))
		cur.execute("insert into articles (title,body,author) values (%s,%s,%s)", (title,body,authorname['auth']))

		#commit
		mysql.connection.commit()

		#close
		cur.close()

		flash('Article Created','success')

		return redirect(url_for('dashboard'))
	return render_template('add_article.html',form=form)

#Edit Article
@app.route('/edit_article/<string:id>',methods=['GET','POST'])
@is_logged_in
def edit_article(id):
	# Create cursor
	cur=mysql.connection.cursor()

	#get article by id
	result=cur.execute("select * from articles where id=%s", [id])
	article=cur.fetchone()

	#Get form
	form = ArticleForm(request.form)

	#populate article form fields
	form.title.data=article['title']
	form.body.data=article['body']

	if request.method == 'POST' and form.validate():
		title=request.form['title']
		body=request.form['body']

		#Create cursor
		cur=mysql.connection.cursor()

		#Execute
		s="select concat(firstname,' ',LastName) as auth from users where username='" + session['username'] + "'"
		result=cur.execute(s)
		authorname=cur.fetchone()

		#cur.execute("insert into articles (title,body,author) values (%s,%s,%s)", (title,body,session['username']))
		cur.execute("update articles set title=%s, body=%s, author=%s where id= %s", (title,body, authorname['auth'], id))

		#commit
		mysql.connection.commit()

		#close
		cur.close()

		flash('Article Updated','success')
		return redirect(url_for('articles'))
		# return redirect(url_for('dashboard'))
	return render_template('edit_article.html',form=form)

#Delete Article
@app.route('/delete_article/<string:id>', methods=['POST'])
@is_logged_in
def delete_article(id):
	#create cursor
	cur=mysql.connection.cursor()

	#execute
	cur.execute("delete from articles where id=%s", [id])

	#commit
	mysql.connection.commit()

	#close
	cur.close()

	flash('Article deleted','success')

	return redirect(url_for('dashboard'))


#Quiz
#+Quiz form class
class QuizForm(Form):
	# Qnum=SelectField('Question Number',choices=[(y,str(y)) for y in range(1,100)],coerce=int)
	Question = TextAreaField('Question')
	subject=SelectField('Subject',choices=[],coerce=int)
	categories=SelectField('Category',choices=[],coerce=int)
	description=SelectField('Description',choices=[],coerce=int)
	op1=TextAreaField('Choice a')
	op2=TextAreaField('Choice b')
	op3=TextAreaField('Choice c')
	op4=TextAreaField('Choice d')
	op_short=StringField('What is the correct answer?')
#delete staging quiz
@app.route('/delete_staging_quiz/<string:id>',methods=['GET','POST'])
@is_logged_in
@is_admin
def quiz_delete_quiz(id):
	cur=mysql.connection.cursor()
	cur.execute("delete from quiz_staging_questions where qq_number=%s",(id))
	cur.execute("delete from quiz_staging_answers where qq_number=%s",(id))
	mysql.connection.commit()
	# cur.execute("DROP TRIGGER tr")
	cur.execute("CREATE TRIGGER tr AFTER UPDATE ON quiz_staging_questions FOR EACH ROW SET @id:=@id+1")
	cur.execute("ALTER TABLE quiz_staging_questions ADD COLUMN new_id INT NOT NULL AFTER qq_number")
	cur.execute("SET @id=1")
	cur.execute("UPDATE quiz_staging_questions SET new_id=@id")
	cur.execute("DROP TRIGGER tr")
	cur.execute("update quiz_staging_answers a inner join quiz_staging_questions b on b.qq_number=a.qq_number set a.qq_number=b.new_id")
	cur.execute("UPDATE quiz_staging_questions SET qq_number=new_id")
	cur.execute("ALTER TABLE quiz_staging_questions DROP new_id")
	mysql.connection.commit()
	cur.close()
	return redirect(url_for('quiz_Create_new_quiz'))

#+Edit existing quiz set
@app.route('/quiz_modify/<string:id>',methods=['GET','POST'])
@is_logged_in
@is_admin
def quiz_modify_quiz(id):
	form = QuizForm(request.form)
	cur=mysql.connection.cursor()
	app.logger.info('---quiz_set id---')
	app.logger.info(id)

	cur.execute("select * from quiz_sets where qs_id=%s",[id])
	qs_result=cur.fetchone()
	cur.execute("select * from quiz_questions_commit where qs_id=%s",[id])
	qlist=cur.fetchall()

	#retreive category info
	cur.execute("select id,name from ref_subjects order by name")
	result=cur.fetchall()
	form.subject.choices=[(a['id'],a['name']) for a in result]
	cur.execute("select id,name from ref_description order by name")
	result=cur.fetchall()
	form.description.choices=[(a['id'],str(a['name'])) for a in result]
	cur.execute("select id,name from ref_categories order by name")
	result=cur.fetchall()
	form.categories.choices=[(a['id'],a['name']) for a in result]


	title=qs_result['qs_name']
	session['title']=title
	unit_id=qs_result['unit_id']
	session['unit_id']=unit_id

	app.logger.info('--unit id---')
	app.logger.info(unit_id)
	param=request.args.get('edit',default="x")
	combo=""
	correct_answer=""

	if request.method=='GET' and param!='x': #edit view of a question
		result=cur.execute("select * from quiz_questions_commit where qq_number=%s and qs_id=%s",(param,[id]))
		q=cur.fetchone()
		form.Question.data=q['qq_body']
		form.subject.process_data(q['subject_id'])
		form.categories.process_data(q['category_id'])
		form.description.process_data(q['description_id'])
		correct_answer=q['qq_correct_answer']
		result=cur.execute("select * from quiz_answers_commit where qq_number=%s and qs_id=%s",(param,[id]))

		if correct_answer=='s':
			combo="short"
			answers=cur.fetchone()
			form.op_short.data=answers['qa_answer']
		else:
			combo="multi"
			c=0
			answers=cur.fetchall()
			for row in answers:
				if c==0:
					form.op1.data=row['qa_answer']
				elif c==1:
					form.op2.data=row['qa_answer']
				elif c==2:
					form.op3.data=row['qa_answer']
				elif c==3:
					form.op4.data=row['qa_answer']
				c=c+1
		return render_template('quiz_modify.html',form=form,qlist=qlist,correct_answer=correct_answer,combo=combo,qid=param,title=title,uid=unit_id)

	if request.method=='POST':
		question_body=request.form['Question']
		cur=mysql.connection.cursor()
		result=cur.execute("select count(*) as m from quiz_questions_commit where qs_id=%s",[id])
		data=cur.fetchone()
		qn=data['m']+1
		app.logger.info("2aa")
		ans1=request.form['op1']
		ans2=request.form['op2']
		ans3=request.form['op3']
		ans4=request.form['op4']
		app.logger.info("3aa")
		ansShort=request.form['op_short']
		app.logger.info("4aa")
		chklist=request.form.getlist('chk_op')
		subject_id=request.form['subject']
		category_id=request.form['categories']
		description_id=request.form['description']

		c=0
		aa="abcd"
		answer=""
		if len(ansShort)>0:
			answer="s"
		else:
			for value in chklist:
				app.logger.info(value)
				answer=aa[int(value)]
		app.logger.info("5aa")
		if request.form['btnrq']=="Update": #if this was for updating question content
			qid=request.form['post_qid']
			app.logger.info("qid="+qid)

			cur.execute("update quiz_questions_commit set qq_body=%s,qq_correct_answer=%s, subject_id=%s, category_id=%s, description_id=%s where qq_number=%s and qs_id=%s",(question_body,answer,subject_id,category_id,description_id,qid,[id]))
			if answer=="s":
				cur.execute("update quiz_answers_commit set qa_answer=%s where qq_number=%s and qa_answer_number=\"s\" and qs_id=%s",(ansShort,qid,[id]))
			else:
				cur.execute("update quiz_answers_commit set qa_answer=%s where qa_answer_number=%s and qq_number=%s and qs_id=%s",(ans1,'a',qid,[id]))
				cur.execute("update quiz_answers_commit set qa_answer=%s where qa_answer_number=%s and qq_number=%s and qs_id=%s",(ans2,'b',qid,[id]))
				cur.execute("update quiz_answers_commit set qa_answer=%s where qa_answer_number=%s and qq_number=%s and qs_id=%s",(ans3,'c',qid,[id]))
				cur.execute("update quiz_answers_commit set qa_answer=%s where qa_answer_number=%s and qq_number=%s and qs_id=%s",(ans4,'d',qid,[id]))
			mysql.connection.commit()
		elif request.form['btnrq']=="Add a quiz": #if this was for adding a new question
			cur.execute("insert into quiz_questions_commit(qq_body,qq_number,qq_correct_answer,qs_id,subject_id,category_id,description_id) values (%s,%s,%s,%s,%s,%s,%s)",(question_body,qn,answer,[id],subject_id,category_id,description_id))
			if answer=="s":
				cur.execute("insert into quiz_answers_commit(qa_answer,qq_number,qa_answer_number,qs_id) values (%s,%s,'s',%s)",(ansShort,qn,[id]))
			else:
				cur.execute("insert into quiz_answers_commit(qa_answer,qq_number,qa_answer_number,qs_id) values (%s,%s,'a',%s)",(ans1,qn,[id]))
				cur.execute("insert into quiz_answers_commit(qa_answer,qq_number,qa_answer_number,qs_id) values (%s,%s,'b',%s)",(ans2,qn,[id]))
				cur.execute("insert into quiz_answers_commit(qa_answer,qq_number,qa_answer_number,qs_id) values (%s,%s,'c',%s)",(ans3,qn,[id]))
				cur.execute("insert into quiz_answers_commit(qa_answer,qq_number,qa_answer_number,qs_id) values (%s,%s,'d',%s)",(ans4,qn,[id]))
			mysql.connection.commit()
		else: #finished creating quizes
			cur.execute("select count(*) as m from quiz_questions_commit where qs_id=%s",[id])
			c=cur.fetchone()
			cur.execute("update quiz_sets set number_of_questions=%s where qs_id=%s",(c['m'],id))
			mysql.connection.commit()
			cur.close()
			return redirect(url_for('quiz_manager'))
		cur.close()
		return redirect(url_for('quiz_modify_quiz',id=id))
	return render_template('quiz_modify.html',form=form,qlist=qlist,combo=combo,correct_answer=correct_answer)



#+Create and edit staging quiz set
@app.route('/quiz_createquiz',methods=['GET','POST'])
@is_logged_in
@is_admin
def quiz_Create_new_quiz():
	cur=mysql.connection.cursor()
	result=cur.execute("select * from quiz_staging_questions")
	qlist=cur.fetchall()
	form = QuizForm(request.form)
	cur.execute("select id,name from ref_subjects order by name")
	result=cur.fetchall()
	form.subject.choices=[(a['id'],a['name']) for a in result]
	cur.execute("select id,name from ref_description order by name")
	result=cur.fetchall()
	form.description.choices=[(a['id'],str(a['name'])) for a in result]
	cur.execute("select id,name from ref_categories order by name")
	result=cur.fetchall()
	form.categories.choices=[(a['id'],a['name']) for a in result]

	title=session['title']
	unit_id=session['unit_id']
	param=request.args.get('edit',default="x")
	combo=""
	correct_answer=""

	if request.method=='GET' and param!='x': #edit view of a question
		result=cur.execute("select qq_number, qq_body,qq_correct_answer,subject_id,category_id,description_id from quiz_staging_questions where qq_number=%s",(param))
		q=cur.fetchone()
		form.Question.data=q['qq_body']
		form.subject.process_data(q['subject_id'])
		form.categories.process_data(q['category_id'])
		form.description.process_data(q['description_id'])
		correct_answer=q['qq_correct_answer']
		result=cur.execute("select * from quiz_staging_answers where qq_number=%s",(param))
		if correct_answer=='s':
			combo="short"
			answers=cur.fetchone()
			form.op_short.data=answers['qa_answer']
		else:
			combo="multi"
			c=0
			answers=cur.fetchall()
			for row in answers:
				if c==0:
					form.op1.data=row['qa_answer']
				elif c==1:
					form.op2.data=row['qa_answer']
				elif c==2:
					form.op3.data=row['qa_answer']
				elif c==3:
					form.op4.data=row['qa_answer']
				c=c+1
		return render_template('quiz_createquiz.html',form=form,qlist=qlist,correct_answer=correct_answer,combo=combo,qid=param,title=title,uid=unit_id)
	if request.method=='POST':
		question_body=request.form['Question']
		cur=mysql.connection.cursor()
		result=cur.execute("select count(*) as m from quiz_staging_questions")
		data=cur.fetchone()
		qn=data['m']+1
		ans1=request.form['op1']
		ans2=request.form['op2']
		ans3=request.form['op3']
		ans4=request.form['op4']
		ansShort=request.form['op_short']
		chklist=request.form.getlist('chk_op')
		subject_id=request.form['subject']
		category_id=request.form['categories']
		description_id=request.form['description']
		c=0
		aa="abcd"
		answer=""
		if len(ansShort)>0:
			answer="s"
		else:
			for value in chklist:
				app.logger.info(value)
				answer=aa[int(value)]
		if request.form['btnrq']=="Update": #if this was for updating question content
			qid=request.form['post_qid']
			app.logger.info("qid="+qid)

			cur.execute("update quiz_staging_questions set qq_body=%s,qq_correct_answer=%s, subject_id=%s, category_id=%s, description_id=%s where qq_number=%s",(question_body,answer,subject_id,category_id,description_id,qid))
			if answer=="s":
				cur.execute("update quiz_staging_answers set qa_answer=%s where qq_number=%s and qa_answer_number=\"s\"",(ansShort,qid))
			else:
				# app.logger.info("qid="+qid)
				# s="update quiz_staging_answers set qa_answer='"+ans1+"' where qa_answer_number='a' and qq_number="+qid
				# app.logger.info(s)
				# cur.execute(s)
				cur.execute("update quiz_staging_answers set qa_answer=%s where qa_answer_number=%s and qq_number=%s",(ans1,'a',qid))
				cur.execute("update quiz_staging_answers set qa_answer=%s where qa_answer_number=%s and qq_number=%s",(ans2,'b',qid))
				cur.execute("update quiz_staging_answers set qa_answer=%s where qa_answer_number=%s and qq_number=%s",(ans3,'c',qid))
				cur.execute("update quiz_staging_answers set qa_answer=%s where qa_answer_number=%s and qq_number=%s",(ans4,'d',qid))
			mysql.connection.commit()
		elif request.form['btnrq']=="Add a quiz": #if this was for adding a new question
			cur.execute("insert into quiz_staging_questions(qq_body,qq_number,qq_correct_answer,subject_id,category_id,description_id) values (%s,%s,%s,%s,%s,%s)",(question_body,qn,answer,subject_id,category_id,description_id))
			if answer=="s":
				cur.execute("insert into quiz_staging_answers(qa_answer,qq_number,qa_answer_number) values (%s,%s,'s')",(ansShort,qn))
			else:
				cur.execute("insert into quiz_staging_answers(qa_answer,qq_number,qa_answer_number) values (%s,%s,'a')",(ans1,qn))
				cur.execute("insert into quiz_staging_answers(qa_answer,qq_number,qa_answer_number) values (%s,%s,'b')",(ans2,qn))
				cur.execute("insert into quiz_staging_answers(qa_answer,qq_number,qa_answer_number) values (%s,%s,'c')",(ans3,qn))
				cur.execute("insert into quiz_staging_answers(qa_answer,qq_number,qa_answer_number) values (%s,%s,'d')",(ans4,qn))
			mysql.connection.commit()
		else: #finished creating quizes
			qf=unit_id+title
			cur.execute("insert into quiz_sets (qs_name,qs_type,unit_id,number_of_questions,quizfile) values (%s,%s,%s,%s,%s)",(title,'Multi-choice',unit_id,(qn-1),qf))
			mysql.connection.commit()
			cur.execute("set @nid=Last_Insert_ID()")
			cur.execute("insert into quiz_questions_commit (qq_body,qq_number,qq_correct_answer,qs_id,subject_id,category_id,description_id) select qq_body,qq_number,qq_correct_answer, @nid,subject_id,category_id,description_id from quiz_staging_questions")
			cur.execute("insert into quiz_answers_commit (qa_answer,qq_number,qa_answer_number,qs_id) select qa_answer,qq_number,qa_answer_number, @nid from quiz_staging_answers")
			mysql.connection.commit()

			cur.execute("delete from quiz_staging_questions")
			cur.execute("delete from quiz_staging_answers")
			mysql.connection.commit()
			cur.close()
			return redirect(url_for('quiz_manager'))
		cur.close()
		return redirect(url_for('quiz_Create_new_quiz'))
	return render_template('quiz_createquiz.html',form=form,qlist=qlist,combo=combo,correct_answer=correct_answer)

#Courses
#+Register form class
class CourseForm(Form):
	name = StringField('Course Name', [validators.Length(min=1, max=100)])
	desc = TextAreaField('Course Description', [validators.Length(min=1)])
	sd=DateField('Starting Date',format='%Y-%m-%d')
	ed=DateField('Ending Date',format='%Y-%m-%d')

	# year=SelectField('Course Year',choices=[('2017', '2017'), ('2018', '2018'), ('2019', '2019')],coerce=int)

	years = [(y, str(y)) for y in reversed(range(2017, 2027))]
	#years.insert(0, ('','year'))
	year = SelectField(choices=years, coerce=int)

	semester=SelectField('Semester',choices=[(1, '1'), (2, '2')], coerce=int)
	status=SelectField('Status',choices=[('Draft','Draft'),('Deleted','Deleted'),('Active','Active')])

	selected_units=StringField('linked_units')
	#unit= SelectMultipleField(u'Units', coerce=int, option_widget=widgets.CheckboxInput(), widget=widgets.ListWidget(html_tag='ul', prefix_label=False))
	# unit=SelectMultipleField('Units',coerce=int)

	# unit = SelectMultipleField(u'Units', coerce=int,
	# 							option_widget=widgets.CheckboxInput(),
	# 							widget=widgets.TableWidget())
    #     						#widget=widgets.ListWidget(html_tag='ul', prefix_label=False))


#+Course enrolment
@app.route('/enrol_course/<string:id>',methods=['POST'])
@is_logged_in
def enrol_course(id):
	#create cursor
	cur=mysql.connection.cursor()

	#see if withdrawal record exists in people_units.
	result=cur.execute("select * from people_units where course_id=%s and people_id=%s",([id],session['id']))
	rs=cur.fetchall()
	if result>0:
		for r in rs:
			if r['status']!="Active":
				cur.execute("update people_units set status='Active' where course_id=%s and people_id=%s",([id],session['id']))

	else: #if this is a new enrolment, fo the followings
		#get the list of linked units for the course_id
		result=cur.execute("select cul_child from course_unit_links where cul_parent=%s",([id]))
		unitslist=cur.fetchall()

		#If linked units exist, add those units to people_units too.
		#if there are no linked units, just add the course enrolment
		if result>0:
			for u in unitslist:
				cur.execute("insert into people_units (unit_id,course_id,people_id,status) values (%s,%s,%s,'Active')", (u['cul_child'],[id],session['id']))
		else:
			cur.execute("insert into people_units (course_id,people_id,status) values (%s,%s,'Active')", ([id],session['id']))

	#commit
	mysql.connection.commit()


	#close
	cur.close()

	flash('Course Enrolled','success')
	return redirect(url_for('courses'))

#withdraw from course
@app.route('/withdraw_course/<string:id>',methods=['POST'])
@is_logged_in
def withdraw_course(id):
	#create cursor
	cur=mysql.connection.cursor()

	#get the list of linked units for the course_id
	result=cur.execute("select pu_id from people_units where course_id=%s and people_id=%s",([id],session['id']))
	unitslist=cur.fetchall()

	#execute
	if result>0:
		cur.execute("update people_units set status='Withdrawal' where course_id=%s and people_id=%s",([id],session['id']))
		mysql.connection.commit()
	cur.close
	flash('Withdrawn from the course','success')
	return redirect(url_for('courses'))

#+Courses list
@app.route('/courses')
@is_logged_in
def courses():
	#create cursor
	cur=mysql.connection.cursor()

	#get my courses
	s="select * from courses where exists(select 1 from people_units where people_units.course_id=courses.id and status='Active' and people_units.people_id={})".format(session['id'])
	# s="select courses.*,pu.pu_id,pu.people_id from courses inner join people_units pu on pu.course_id=courses.id  inner join people p on p.id=pu.people_id where p.username='"+session['username']+"'"
	app.logger.info(s)
	result=cur.execute(s)
	courses=cur.fetchall()

	#get not yet enrolled courses
	s="select * from courses where not exists(select 1 from people_units where people_units.course_id=courses.id and people_units.people_id={}) or exists(select 1 from people_units where people_units.course_id=courses.id and people_units.people_id={} and status='Withdrawal')".format(session['id'],session['id'])
	result=cur.execute(s)
	opencourses=cur.fetchall()

	if result > 0:
		return render_template('courses.html', courses=courses,opencourses=opencourses, pid=session['id'])
	else:
		msg='No courses found'
		return render_template('dashboard'.html, msg=msg)

	#close connection
	cur.close()

#+single course
@app.route('/course/<string:id>/')
def course(id):
	#create cursor
	cur=mysql.connection.cursor()

	#get course
	result=cur.execute("select * from courses where id =  %s", [id])
	course=cur.fetchone()
	result=cur.execute("SELECT u.* FROM course_unit_links cul inner join units u on u.id=cul.cul_child " +
						"where cul.cul_parent=%s",[id])
	unitlist=cur.fetchall()

	#check if the user has enrolled already
	result=cur.execute("select pu_id from people_units where course_id=%s and people_id=%s and status='Active'",([id],session['id']))
	enrolled=False
	if result>0:
		enrolled=True

	return render_template('course.html', course=course,unitlist=unitlist,cid=id,enrolled=enrolled)


#+Edit Course
@app.route('/edit_course/<string:id>',methods=['GET','POST'])
@is_admin
def edit_course(id):

	# Create cursor
	cur=mysql.connection.cursor()

	#get course by id
	result=cur.execute("select * from courses where id=%s", [id])
	course=cur.fetchone()

	#Get form
	form = CourseForm(request.form)

	#populate Course form fields
	form.name.data=course['course_name']
	form.desc.data=course['course_desc']
	# sd=form.sd_year.data + '-' + form.sd_month.data +'-'+ form.sd_day.data
	# ed=form.ed_year.data + '-' + form.ed_month.data +'-'+ form.ed_day.data
	form.sd.data=course['start_date']
	form.ed.data=course['end_date']

	form.year.data=course['year']
	form.semester.data=course['semester']

	form.status.data=course['status']

	#get Linked units by course id
	result=cur.execute("SELECT u.* from course_unit_links cul inner join units u on u.id=cul.cul_child where cul.cul_parent=%s",[id])
	unitlist=cur.fetchall()

	#Convert dict unit ids into string
	WasLinkedIDs=','.join(str(u['id']) for u in unitlist)

	#get Unlinked units by course id
	result=cur.execute("SELECT u.* from units u Where not exists(select cul_child from course_unit_links where cul_parent=%s and u.id=cul_child)",[id])
	unitlist_unlinked=cur.fetchall()
	cur.close()


	if request.method == 'POST' and form.validate():

		#get the linked units
		linkedUnits=request.form.getlist('chk_linkedunits')
		Linked_IDs=','.join(str(x) for x in linkedUnits)

		#get the new linked units and merge with Linked_IDs
		unlinkedUnits=request.form.getlist('chk_unlinkedunits')
		newids=','.join(str(x) for x in unlinkedUnits)

		app.logger.info("Originally linked units:"+WasLinkedIDs)
		app.logger.info("Units that are still being checked:"+Linked_IDs)
		app.logger.info("new checked units:"+newids)

		if len(newids)>=1:
			Linked_IDs=Linked_IDs + "," + newids

		#Compare Old linked IDs and new linked ids and return the difference
		Now_Unlinked_IDs=set(WasLinkedIDs.split(","))-set(Linked_IDs)


		app.logger.info("All checked units:"+Linked_IDs)
		app.logger.info("units that are now unlinked:"+str(Now_Unlinked_IDs))

		cur=mysql.connection.cursor()
		# for str(x) in linkedUnits:


		for u_id in Linked_IDs.split(","):
			if len(u_id)>0:
				result=cur.execute("select count(1) as m from course_unit_links where cul_parent=%s and cul_child=%s",([id],u_id))
				dbcount=cur.fetchone()
				if dbcount['m']<=0:
					cur.execute("insert into course_unit_links (cul_parent,cul_child) values (%s,%s)",([id],u_id))

		for u_id in Now_Unlinked_IDs:
			result=cur.execute("select count(1) as m from course_unit_links where cul_parent=%s and cul_child=%s",([id],u_id))
			dbcount=cur.fetchone()
			if dbcount['m']>0:
				cur.execute("delete from course_unit_links where cul_parent=%s and cul_child=%s",([id],u_id))

		# 	return redirect(url_for('courses'))
		# return render_template('edit_course.html',form=form, unitlist=unitlist,unitlist_unlinked=unitlist_unlinked)

		name=request.form['name']
		desc=request.form['desc']
		sd=request.form['sd']
		ed=request.form['ed']
		status=request.form['status']
		year=request.form['year']
		semester=request.form['semester']

		#Create cursor
		cur=mysql.connection.cursor()

		#Execute
		cur.execute("update courses set course_name=%s, course_desc=%s, status=%s, start_date=%s, end_date=%s, year=%s, semester=%s where id=%s", (name,desc,status,sd,ed,year,semester,[id]))

		#commit
		mysql.connection.commit()

		#close
		cur.close()

		flash('Course Updated','success')
		return redirect(url_for('courses'))

	return render_template('edit_course.html',form=form, unitlist=unitlist,unitlist_unlinked=unitlist_unlinked)


#+Create Courses
@app.route('/create_course', methods=['GET','POST'])
@is_admin
def create_course():
	form = CourseForm(request.form)

	#update unit multiselect field
	cur=mysql.connection.cursor()
	result=cur.execute("select * from units")
	units_list=cur.fetchall()
	# form.unit.choices=[(r['id'],r['unit_name']) for r in units_list]
	cur.close()

	if request.method == 'POST' and form.validate():
		name=form.name.data
		desc=form.desc.data
		# sd=form.sd_year.data + '-' + form.sd_month.data +'-'+ form.sd_day.data
		# ed=form.ed_year.data + '-' + form.ed_month.data +'-'+ form.ed_day.data
		sd=form.sd.data
		ed=form.ed.data
		status=form.status.data
		year=form.year.data
		semester=form.semester.data
		# units=form.unit.data

		#Create cursor
		cur=mysql.connection.cursor()

		#Execute

		cur.execute("insert into courses (course_name,course_desc,status,start_date,end_date,year,semester,created_by,created_username) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)", (name,desc,status,sd,ed,year,semester,session['fullname'],session['username']))

		#commit
		mysql.connection.commit()

		#Insert course_unit links
		#+get the checked units
		linkedUnits=request.form.getlist('chk_linkedunits')
		newids=','.join(str(x) for x in linkedUnits)

		#+get the course id
		cur.execute("select max(id) as m from courses ")
		cid=cur.fetchone()
		new_course_id=cid['m']

		#+now insert new course_unit_links
		for u_id in newids.split(","):
			cur.execute("insert into course_unit_links (cul_parent,cul_child) values (%s,%s)",(new_course_id,u_id))

		mysql.connection.commit()

		#close
		cur.close()

		flash('Course Created','success')

		return redirect(url_for('dashboard'))
	return render_template('create_course.html',form=form,units_list=units_list)


#units
#+Unit form class
class UnitForm(Form):
	subject=SelectField('Subject',coerce=int)
	name = StringField('Unit Name', [validators.Length(min=1, max=100)])
	desc = TextAreaField('Unit Description', [validators.Length(min=1)])
	sd=DateField('Starting Date',format='%Y-%m-%d')
	ed=DateField('Ending Date',format='%Y-%m-%d')
	years = [(y, str(y)) for y in reversed(range(2017, 2027))]
	year = SelectField(choices=years, coerce=int)
	semester=SelectField('Semester',choices=[(1, '1'), (2, '2')], coerce=int)
	status=SelectField('Status',choices=[('Draft','Draft'),('Deleted','Deleted'),('Active','Active')])
	selected_units=StringField('linked_courses')

#+Edit Unit
@app.route('/edit_unit/<string:id>',methods=['GET','POST'])
@is_admin
def edit_unit(id):
	#Get form
	form = UnitForm(request.form)
	# Create cursor
	cur=mysql.connection.cursor()

	#get the refs
	result=cur.execute("select * from ref_subjects order by name")
	ref_subjects=cur.fetchall()
	form.subject.choices = [(c['id'], c['name']) for c in ref_subjects]

	#get unit by id
	result=cur.execute("select * from units where id=%s", [id])
	unit=cur.fetchone()



	#populate Unit form fields
	form.subject.process_data(unit['subject'])
	form.name.data=unit['unit_name']
	form.desc.data=unit['unit_desc']
	form.sd.data=unit['start_date']
	form.ed.data=unit['end_date']
	form.year.data=unit['year']
	form.semester.data=unit['semester']
	form.status.data=unit['status']

	#get Linked courses by unit id
	result=cur.execute("SELECT c.* FROM course_unit_links cul inner join courses c on c.id=cul.cul_parent " +
						"where cul.cul_child=%s",[id])
	courselist=cur.fetchall()

	#get linked quizes
	result=cur.execute("select * from quiz_sets where unit_id=%s",[id])
	quizlist=cur.fetchall()

	#Convert dict quiz ids into string
	WasLinkedIDs=','.join(str(u['qs_id']) for u in quizlist)

	#get Unlinked quizes by unit id
	result=cur.execute("SELECT u.* from quiz_sets u Where u.unit_id is null")
	quizlist_unlinked=cur.fetchall()

	#close cursor
	cur.close()

	if request.method == 'POST' and form.validate():

		#get the linked quizes
		linkedQuizes=request.form.getlist('chk_linkedquizes')
		Linked_IDs=','.join(str(x) for x in linkedQuizes)

		#get the new linked units and merge with Linked_IDs
		unlinkedQuizes=request.form.getlist('chk_unlinkedquizes')
		newids=','.join(str(x) for x in unlinkedQuizes)

		app.logger.info("Originally linked Qz:"+WasLinkedIDs)
		app.logger.info("Qzs that are still being checked:"+Linked_IDs)
		app.logger.info("new checked Qz:"+newids)

		if len(Linked_IDs)>=1:
			if len(newids)>=1:
				Linked_IDs=Linked_IDs + "," + newids
			else:
				Linked_IDs=Linked_IDs
		else:
			Linked_IDs=newids

		#Compare Old linked IDs and new linked ids and return the difference
		Now_Unlinked_IDs=set(WasLinkedIDs.split(","))-set(Linked_IDs)


		app.logger.info("All checked Qzs:"+Linked_IDs)
		app.logger.info("Qzs that are now unlinked:"+str(Now_Unlinked_IDs))

		#create cursor
		cur=mysql.connection.cursor()

		for q_id in Linked_IDs.split(","):
			if len(q_id)>0: #if the quiz has no unit_id then assign the unit_id to the quiz_set
				app.logger.info("add new unit_id into qs:"+q_id+", unit_id="+id)
				result=cur.execute("select count(qs_id) as m from quiz_sets where unit_id is null and qs_id=%s",(q_id))
				dbcount=cur.fetchone()
				if dbcount['m']>0:
					cur.execute("update quiz_sets set unit_id=%s where qs_id=%s",([id],q_id))
					mysql.connection.commit()

		for q_id in Now_Unlinked_IDs: #if the quiz was linked and not unlinked, unassign the unit_id from the quiz set
			result=cur.execute("select count(qs_id) as m from quiz_sets where unit_id=%s and qs_id=%s",([id],q_id))
			dbcount=cur.fetchone()
			if dbcount['m']>0:
				app.logger.info("null candidate:"+q_id)
				cur.execute("update quiz_sets set unit_id = NULL where qs_id in ("+q_id+")")
				mysql.connection.commit()

		name=request.form['name']
		desc=request.form['desc']
		sd=request.form['sd']
		ed=request.form['ed']
		status=request.form['status']
		year=request.form['year']
		semester=request.form['semester']
		subject=request.form['subject']

		#Execute
		s=("update units set subject=%s,units_name=%s,units_desc=%s,status=%s,start_date=%s,end_date=%s,year=%s,semester=%s) where id=%s", (subject,name,desc,status,sd,ed,year,semester,[id]))
		app.logger.info(s)
		cur.execute("update units set subject="+subject+",unit_name=%s,unit_desc=%s,status=%s,start_date=%s,end_date=%s,year=%s,semester=%s where id="+str(id), (name,desc,status,sd,ed,year,semester))

		#commit
		mysql.connection.commit()



		flash('Unit Updated','success')
		return redirect(url_for('units'))

	return render_template('edit_unit.html',form=form, courselist=courselist, quizlist=quizlist, quizlist_unlinked=quizlist_unlinked)


#+Create Units
@app.route('/create_unit', methods=['GET','POST'])
@is_admin
def create_Unit():
	form = UnitForm(request.form)

	# Create cursor
	cur=mysql.connection.cursor()

	#get the refs
	result=cur.execute("select * from ref_subjects order by name")
	ref_subjects=cur.fetchall()
	form.subject.choices = [(c['id'], c['name']) for c in ref_subjects]
	cur.close()
	#update unit multiselect field
	# cur=mysql.connection.cursor()
	# result=cur.execute("select * from courses")
	# course_lisr=cur.fetchall()
	# cur.close()

	if request.method == 'POST' and form.validate():
		name=form.name.data
		desc=form.desc.data
		# sd=form.sd_year.data + '-' + form.sd_month.data +'-'+ form.sd_day.data
		# ed=form.ed_year.data + '-' + form.ed_month.data +'-'+ form.ed_day.data
		sd=form.sd.data
		ed=form.ed.data
		status=form.status.data
		year=form.year.data
		semester=form.semester.data
		subject=form.subject.data
		# units=form.unit.data

		#Create cursor
		cur=mysql.connection.cursor()

		#Execute

		cur.execute("insert into units (unit_name,unit_desc,status,start_date,end_date,year,semester,subject) values (%s,%s,%s,%s,%s,%s,%s,%s)", (name,desc,status,sd,ed,year,semester,subject))

		#commit
		mysql.connection.commit()

		# #Insert course_unit links
		# cur.execute("select max(id) as m from courses ")
		# cid=cur.fetchone()
		# new_course_id=cid['m']
		# for u in units:
		# 	cur.execute("insert into course_unit_links (cul_parent,cul_child) values (%s,%s)",(new_course_id,u))
		# mysql.connection.commit()

		#close
		cur.close()

		flash('Unit Created','success')

		return redirect(url_for('units'))
	return render_template('create_unit.html',form=form)


#+Units list
@app.route('/units')
def units():
	#create cursor
	cur=mysql.connection.cursor()

	#get my courses
	s=  'SELECT u.id,    u.unit_name,    u.unit_desc,    u.status,    u.start_date, ' \
	    + 'u.end_date,    u.year,    u.semester,    r_sbj.name as subject,    coalesce(x.m,0) as qcount ' \
		+ 'FROM units u left join (select unit_id,count(qs_id) as m from quiz_sets group by unit_id) x on x.unit_id=u.id ' \
		+ 'left join ref_subjects r_sbj on r_sbj.id=u.subject ' \
	  	+ 'order by subject, year, semester desc'
	result=cur.execute(s)
	units=cur.fetchall()
	#close connection
	cur.close()
	if result > 0:
		return render_template('units.html', units=units)
	else:
		msg='No courses found'
		return render_template('units'.html, msg=msg, units=units)


#+single unit
@app.route('/unit/<string:id>/')
def unit(id):

	#create cursor
	cur=mysql.connection.cursor()

	#get unit
	result=cur.execute("select * from units where id =  %s", [id])
	unit=cur.fetchone()

	#get linked courses
	result=cur.execute("SELECT c.* FROM course_unit_links cul inner join courses c on c.id=cul.cul_parent " +
						"where cul.cul_child=%s",[id])
	courselist=cur.fetchall()

	#get quizes
	result=cur.execute("select * from quiz_sets where unit_id=%s",[id])
	quizlist=cur.fetchall()
	cur.close()

	#get people_unit ID
	cid=request.args.get('cid')
	pu_id=get_pu_id(cid,id,session['id'])

	#set session's question index number
	session['qidx']=0
	session['correct']=0
	session['answers']=["x" for i in range(100)]
	session['useranswers']=["" for i in range(100)]
	session['pu_id']=pu_id
	return render_template('unit.html', unit=unit,courselist=courselist, quizlist=quizlist,pu_id=pu_id)

@app.route('/quiz_solve/<string:id>',methods=['GET','POST'])
def quiz_solve(id):
	#get the quiz set ID
	cur=mysql.connection.cursor()
	puid=session['pu_id']
	qno=request.args.get('q',default=0)
	result=cur.execute("select * from quiz_sets where qs_id=%s",[id])
	qset=cur.fetchone()
	session['totalq']=qset['number_of_questions']
	session['qs_id']=id
	#get the question by index number (starting from 0)
	result=cur.execute("select qq_number,qq_body,qq_correct_answer from quiz_questions_commit where qs_id=%s",[id])
	quizes=cur.fetchall()
	x=0

	#if navigated to other questions, this will be triggered
	if int(qno)>0:
		session['qidx']=int(qno)-1
		return redirect(request.path)
	if session['qidx']==session['totalq']:
		app.logger.info(session['qidx'])
		return render_template('quiz_solve.html',mark=session['answers'].count('o'), qsid=id,qset=qset,question=None,choices=None,finished=True)
	question=quizes[session['qidx']]

	#if answer was clicked, move to next question
	if request.method=='POST':
		app.logger.info("POST CALLED")
		if request.form['btnrq']=="Go back to your Dashboard":
			app.logger.info("finished test")
			return redirect(url_for('dashboard'))
			# return redirect(url_for("get_jsdata"))

		#Get user answers and compare with the correct answer
		cor_answ=question['qq_correct_answer']
		if cor_answ=='s':
			cur.execute("select qa_answer from quiz_answers_commit where qs_id=%s and qq_number=%s",([id],(session['qidx']+1)))
			cor_answ=cur.fetchone()['qa_answer']
		std_answ=request.form['answerGroup']
		session['useranswers'][session['qidx']]=std_answ
		app.logger.info(session['useranswers'])

		if cor_answ==std_answ:
			session['answers'][int(session['qidx'])]="o"
		else:
			session['answers'][int(session['qidx'])]="x"

		#if reached the last question has been solved, end the quizes
		if session['qidx']+1==session['totalq']:
			#submit test result
			submit_test_result()
			return render_template('quiz_solve.html',mark=session['answers'].count('o'), qsid=None,qset=qset,question=None,choices=None,finished=True)
		session['qidx']+=1

		result=cur.execute("select qq_number,qq_body,qq_correct_answer from quiz_questions_commit where qs_id=%s",[id])
		quizes=cur.fetchall()
		question=quizes[session['qidx']]
		cur.execute("select b.qa_answer_number, b.qa_answer from quiz_answers_commit b where b.qs_id=%s and b.qq_number=%s",([id],question['qq_number']))
		choices=cur.fetchall()
		cur.close()
		return render_template('quiz_solve.html',qsid=id,qset=qset,question=question,choices=choices,finished=False)

	# session['CorrectChoice']=quizes[session['qidx']]['qq_correct_answer']
	cur.execute("select b.qa_answer_number, b.qa_answer from quiz_answers_commit b where b.qs_id=%s and b.qq_number=%s",(id,question['qq_number']))
	choices=cur.fetchall()

	cur.close()

	return render_template('quiz_solve.html',qsid=id,qset=qset,question=question,choices=choices,finished=False)
@app.route('/quiz_template')
def quiz_examples():
	return render_template('quiz_template.html')
#
@app.route('/quiz_template_original/<string:id>/')
def quiz_template_original(id):
	cur=mysql.connection.cursor()
	result=cur.execute("select * from quiz_sets where qs_id=%s",[id])
	quiz=cur.fetchone()
	cur.close()
	return render_template('quiz_template_original.html',quiz=quiz)

@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)

@app.route('/users')
@is_admin
def users():
	cur=mysql.connection.cursor()
	s="select username,firstname,lastname,email,mob,date_of_birth,phone,people_type from people where exists (select 1 from users where power_level='student' and users.username=people.username)"
	result=cur.execute(s)
	users=cur.fetchall()
	cur.close()
	return render_template('users.html',users=users)

# @app.route('/posttestresult',methods=['POST'])
# def get_post_js_data():
# 	jsdata=request.form['javascript_data']
# 	s=json.loads(jsdata)[0]
# 	app.logger.info(s)
# 	return s

@app.route('/getdata', methods=['GET','POST'])
def get_jsdata():

	qs_id=session['qs_id']
	correct=session['answers'].count('o')
	total=session['totalq']

	#this variable holds correct/wrong info in a line of string such as oxoxoooxxxx
	answers="".join(session['answers'][0:total])

	#this variable holds a list of user's answers
	useranswers=session['useranswers'][0:total]
	pu_id=session['pu_id']
	num_attempt=0
	app.logger.info(qs_id)
	app.logger.info(correct)
	app.logger.info(total)
	app.logger.info(answers)

	cur=mysql.connection.cursor()
	# s="select count(qr_id) as n from quiz_record where qs_id={} and people_id={}".format(qs_id,session['id'])
	# app.logger.info(s)
	result=cur.execute("select count(qr_id) as n from quiz_record where qs_id=%s and pu_id=%s",(qs_id,pu_id))
	rs=cur.fetchone()
	num_attempt=rs['n']+1

	#insert quiz results to quiz_record table
	ss="insert into quiz_record(qs_id,qr_correct,qr_total,qr_attempt,qr_answered,people_id,pu_id) values ({},{},{},{},'{}',{},{})".format(qs_id,correct,total,num_attempt,answers,session['id'],pu_id)
	app.logger.info(ss)
	cur.execute(ss)
	mysql.connection.commit()

	#insert quiz and peopel_unit links
	result=cur.execute("insert into people_unit_quiz_link (pu_id,qs_id,qr_id) values (%s,%s,last_insert_id())",(pu_id,qs_id))
	mysql.connection.commit()

	cur.close()
	flash('Quiz Record update','success')
	return redirect('dashboard')

def submit_test_result():

	qs_id=session['qs_id']
	correct=session['answers'].count('o')
	total=session['totalq']

	#this variable holds correct/wrong info in a line of string such as oxoxoooxxxx
	answers="".join(session['answers'][0:total])

	#this variable holds a list of user's answers
	useranswers=session['useranswers'][0:total]
	pu_id=session['pu_id']
	num_attempt=0
	app.logger.info(qs_id)
	app.logger.info(correct)
	app.logger.info(total)
	app.logger.info(answers)

	cur=mysql.connection.cursor()
	# s="select count(qr_id) as n from quiz_record where qs_id={} and people_id={}".format(qs_id,session['id'])
	# app.logger.info(s)
	result=cur.execute("select count(qr_id) as n from quiz_record where qs_id=%s and pu_id=%s",(qs_id,pu_id))
	rs=cur.fetchone()
	num_attempt=rs['n']+1

	#insert quiz results to quiz_record table
	ss="insert into quiz_record(qs_id,qr_correct,qr_total,qr_attempt,qr_answered,people_id,pu_id,percent) values ({},{},{},{},'{}',{},{},{})".format(qs_id,correct,total,num_attempt,answers,session['id'],pu_id,(correct/total)*100)
	app.logger.info(ss)
	cur.execute(ss)
	mysql.connection.commit()

	#get the quiz record ID which was just inserted to table
	cur.execute("set @qrid=last_insert_id()")
	for num,answer in enumerate(useranswers,start=1):
		app.logger.info("useranswers="+answer)
		cur.execute("insert into quiz_user_answers (qr_id,question_number,user_answer) values (@qrid,%s,%s)",(num,answer))

	#insert quiz and peopel_unit links
	result=cur.execute("insert into people_unit_quiz_link (pu_id,qs_id,qr_id) values (%s,%s,@qrid)",(pu_id,qs_id))
	mysql.connection.commit()

	cur.close()
	flash('Quiz Record update','success')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/quiz_manager', methods=['GET', 'POST'])
def quiz_manager():
	cur=mysql.connection.cursor()
	result=cur.execute("select u.id, u.unit_name,qs.* from units u left join quiz_sets qs on qs.unit_id=u.id order by u.id")
	rs=cur.fetchall()

	if request.method=='POST':
		if request.form['btnrq']=='Remove Quiz':
			qs_id=request.form['post_qid']
			app.logger.info("qs_id:"+qs_id)
			cur.execute("delete from quiz_sets where qs_id="+qs_id)
			flash("Quiz delete",'success')
			mysql.connection.commit()
			cur.close()
			return redirect(request.url)
		#Create new quiz_set

		# unit_id=request.form['post_id']
		# title=request.form['qtitle']
		# return redirect(url_for('quiz_Create_new_quiz',uid=unit_id,title=title))
		session['unit_id']=request.form['post_id']
		session['title']=request.form['qtitle']
		return redirect(url_for('quiz_Create_new_quiz'))
	return render_template('quiz_manager.html',qlist=rs)

@is_logged_in
@app.route('/MyProgress',methods=['GET','POST'])
def MyProgress():
	cur=mysql.connection.cursor()



# def upload_file():
#     cur=mysql.connection.cursor()
#     result=cur.execute("select u.id, u.unit_name,qs.* from units u left join quiz_sets qs on qs.unit_id=u.id order by u.id")
#     rs=cur.fetchall()
#     if request.method == 'POST':
#
#         if request.form['btnrq']=="Remove Quiz":
#             qs_id=request.form['post_qid']
#             app.logger.info("qs_id:"+qs_id)
#             cur.execute("delete from quiz_sets where qs_id="+qs_id)
#             flash("Quiz delete",'success')
#             mysql.connection.commit()
# 			  cur.close()
#             return redirect(request.url)
#         elif 'file' not in request.files:
#             flash('No file part','danger')
#             return redirect(request.url)
#
#         # check if the post request has the file part
#         file = request.files['file']
#         # if user does not select file, browser also
#         # submit a empty part without filename
#         if file.filename == '':
#             flash('No selected file','danger')
#             return redirect(request.url)
#         if file and allowed_file(file.filename):
#             filename = secure_filename(file.filename)
#             if ".json" in filename:
#                 app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER_QUIZ
#
#                 #now insert the database to assign the question
#                 buttonid=request.form['post_id']
#                 cur.execute("insert into quiz_sets (qs_name,qs_type,unit_id,number_of_questions,quizfile) values (%s,%s,%s,10,%s)", (filename.replace(".json",""),"Multi-choice",buttonid,filename))
#                 mysql.connection.commit()
#                 file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#                 flash('Quiz Data Uploaded','success')
#             else:
#                 app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER
#                 file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#                 flash('Image uploaded','success')
#             return redirect(url_for('uploaded_file',filename=filename))
#     cur.close()
#     return render_template('quiz_manager.html',qlist=rs)





@app.route('/uploads/<filename>')
def uploaded_file(filename):
    # return send_from_directory(app.config['UPLOAD_FOLDER'],filename)

    return redirect('quiz_manager')

def get_pu_id(cid,uid,pid):
	cur=mysql.connection.cursor()
	result=cur.execute("select pu_id from people_units where course_id=%s and unit_id=%s and people_id=%s",(cid,uid,pid))
	data=cur.fetchone()
	cur.close()
	if result==0:
		return 0
	return data['pu_id']

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.secret_key='secret123'
if __name__ == '__main__':
	app.run(host='192.168.0.6')
	# app.run(debug=True)
