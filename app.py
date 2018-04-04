from flask import Flask
from models import db,UserLogin
from flask import Flask, flash, redirect, render_template, request, session, abort
import os
import json

app = Flask(__name__)


app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://sacco_save:123@localhost:5432/sacco_save'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('index.html')
    else:
        return render_template('home.html')
 
@app.route('/VerifyLogin',methods=['POST'])
def do_admin_login():
	if request.form['account_no'] == '' or request.form['user_pass'] == '':
		return render_template('index.html', my_var=request.args.get('invalid_detail', 'EMPTY_FIELDS'))	
	else:	
		try:
			my_user=db.session.query(UserLogin).filter_by(nu_account_no=request.form['account_no'],vc_pass_word=request.form['user_pass']).first()
			if my_user is not None:
				session['logged_in']=True
				session['account_no']=my_user.nu_account_no
				session['full_name']=my_user.vc_full_name
				return home()
			else:
				pass
	    		return render_template('index.html', my_var=request.args.get('invalid_detail', 'INVALID_USER'))
		except:
			pass
        	return render_template('index.html', my_var=request.args.get('invalid_detail', 'INVALID_USER'))

@app.route("/logout")
def logout():
    #logout user
    session['logged_in'] = False
    return home() 
 
 
if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='0.0.0.0', port=4000)
