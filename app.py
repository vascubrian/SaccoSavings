from flask import Flask
from models import db,UserLogin,DepositList,LoanList
from flask import Flask, flash, redirect, render_template, request, session, abort
import os
import json
from sqlalchemy.sql import func

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
    	#fetching saving data.................
    	qry_sum_dep = db.session.query(func.sum(DepositList.nu_amt).label("sum_amt")).filter_by(nu_account_no=session['account_no']).all()
    	my_saving=db.session.query(DepositList).filter_by(nu_account_no=session['account_no']).order_by(DepositList.dt_date).all()
        return render_template('home.html',my_deposit=my_saving,qry_sum_dep=qry_sum_dep)
 
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
				session['user_type']=my_user.user_type
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

@app.route("/SwitchPanel")
def SwitchPanel():

    return render_template('home.html', my_var=request.args.get('my_var', ''),my_member=UserLogin.query.order_by(UserLogin.nu_account_no).all(),my_all_dep=DepositList.query.order_by(DepositList.nu_account_no).all(),dep_sum_all = db.session.query(func.sum(DepositList.nu_amt).label("sum_amt")).all())

@app.route("/EnrollMember",methods=['POST'])
def EnrollMember():
	if request.form['account_no']=='' or request.form['full_name']=='':
		return render_template('home.html', my_var=request.args.get('AddMember', 'EMPTY_FIELDS'))
	else:
		try:
			my_user=db.session.query(UserLogin).filter_by(nu_account_no=request.form['account_no']).first()
			if my_user is not None:				
				return render_template('home.html', my_var=request.args.get('AddMember', 'EXISTS'))
			else:
				add_data=UserLogin(request.form['account_no'],request.form['reg_date'],request.form['full_name'],request.form['gender'],request.form['contact'],request.form['address'],request.form['password'],request.form['user_type'],request.form['email'])
				db.session.add(add_data)
				db.session.commit()            
				pass
	    		return render_template('home.html', my_var=request.args.get('AddMember', 'SUCCESS-REG'))

		except:
			pass
        	return render_template('home.html', my_var=request.args.get('AddMember', 'INVALID_ENTRY'))

@app.route("/FilterDeposit",methods=['POST'])
def FilterDeposit():
	if request.form['account_no']=='' or request.form['amt']=='' or request.form['reg_date']=='':
		return render_template('home.html', my_var=request.args.get('FilterDeposit', 'DEP-EMPTY_FIELDS'))
	else:
		try:
			my_user=db.session.query(UserLogin).filter_by(nu_account_no=request.form['account_no']).first()
			if my_user is None:				
				return render_template('home.html', my_var=request.args.get('FilterDeposit', 'DEP-EXISTS'))
			else:
				add_data=DepositList(request.form['account_no'],request.form['amt'],request.form['reg_date'],request.form['deposited_by'],request.form['cashier_name'])
				db.session.add(add_data)
				db.session.commit()            
				pass
				qry_sum_dep = db.session.query(func.sum(DepositList.nu_amt).label("sum_amt")).filter_by(nu_account_no=session['account_no']).all()
				my_saving=db.session.query(DepositList).filter_by(nu_account_no=session['account_no']).order_by(DepositList.dt_date).all()
	    		return render_template('home.html', my_var=request.args.get('FilterDeposit', 'SUCCESS-DEP'),my_deposit=my_saving,qry_sum_dep=qry_sum_dep)

		except:
			pass
        	return render_template('home.html', my_var=request.args.get('FilterDeposit', 'DEP-INVALID_ENTRY'))
@app.route("/AddLoan",methods=['POST'])
def AddLoan():
	if request.form['account_no']=='' or request.form['amt']=='' or request.form['reg_date']=='' or request.form['loan_desc']=='':
		return render_template('home.html', my_var=request.args.get('AddLoan', 'LOAN-EMPTY_FIELDS'))
	else:
		try:
			my_user=db.session.query(UserLogin).filter_by(nu_account_no=request.form['account_no']).first()
			if my_user is None:				
				return render_template('home.html', my_var=request.args.get('AddLoan', 'LOAN-EXISTS'))
			else:
				add_data=LoanList(request.form['account_no'],request.form['amt'],request.form['reg_date'],request.form['loan_desc'],request.form['added_by'],request.form['cashier_name'])
				db.session.add(add_data)
				db.session.commit()            
				pass
				qry_sum_dep = db.session.query(func.sum(DepositList.nu_amt).label("sum_amt")).filter_by(nu_account_no=session['account_no']).all()
				my_saving=db.session.query(DepositList).filter_by(nu_account_no=session['account_no']).order_by(DepositList.dt_date).all()
	    		return render_template('home.html', my_var=request.args.get('AddLoan', 'SUCCESS-LOAN'),my_deposit=my_saving,qry_sum_dep=qry_sum_dep)

		except:
			pass
        	return render_template('home.html', my_var=request.args.get('AddLoan', 'LOAN-INVALID_ENTRY'))

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='0.0.0.0', port=4000)
