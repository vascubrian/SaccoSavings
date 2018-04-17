from flask import Flask
from models import db,UserLogin,DepositList,LoanList,CompInfo
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

    	qry_sum_dep = db.session.query(func.sum(DepositList.nu_amt).label("sum_amt")).filter_by(nu_account_no=session['account_no'],vc_comp_code=session['comp_code']).all()
    	my_saving=db.session.query(DepositList).filter_by(nu_account_no=session['account_no'],vc_comp_code=session['comp_code']).order_by(DepositList.dt_date).all()
        #----------------------COMP_INFO.................................
        comp_info=db.session.query(CompInfo).filter_by(vc_comp_code=session['comp_code']).first()
        session['comp_name']=comp_info.vc_comp_name
        session['comp_address']=comp_info.vc_comp_address
        session['comp_abrev']=comp_info.vc_comp_abrev
        session['comp_contact']=comp_info.vc_comp_contact
        session['comp_slogan']=comp_info.vc_comp_slogan
        session['comp_email']=comp_info.vc_email
        session['comp_website']=comp_info.vc_website

        return render_template('home.html',my_deposit=my_saving,qry_sum_dep=qry_sum_dep)
 
@app.route('/VerifyLogin',methods=['POST'])
def do_admin_login():
	if request.form['account_no'] == '' or request.form['user_pass'] == '' or request.form['sacco_code']=='':
		return render_template('index.html', my_var=request.args.get('invalid_detail', 'EMPTY_FIELDS'))	
	else:	
		#try:
			my_user=db.session.query(UserLogin).filter_by(nu_account_no=request.form['account_no'],vc_pass_word=request.form['user_pass'],vc_comp_code=request.form['sacco_code']).first()
			if my_user is not None:
				session['logged_in']=True
				session['account_no']=my_user.nu_account_no
				session['full_name']=my_user.vc_full_name
				session['user_type']=my_user.user_type
				session['comp_code']=my_user.vc_comp_code

				return home()
			else:
				pass
	    		return render_template('index.html', my_var=request.args.get('invalid_detail', 'INVALID_USER'))
		#except:
			#pass
        	#return render_template('index.html', my_var=request.args.get('invalid_detail', 'INVALID_USER'))

@app.route("/logout")
def logout():
    #logout user
    session['logged_in'] = False
    return home() 

@app.route("/SwitchPanel")
def SwitchPanel():
    return render_template('home.html',my_loan=LoanList.query.filter_by(nu_account_no=session['account_no'],vc_cleared_status='NO',vc_comp_code=session['comp_code']).order_by(LoanList.dt_date).all(),loan_all=LoanList.query.filter_by(vc_cleared_status='NO',vc_comp_code=session['comp_code']).order_by(LoanList.dt_date).all(), my_var=request.args.get('my_var', ''),my_member=UserLogin.query.filter_by(vc_comp_code=session['comp_code']).order_by(UserLogin.nu_account_no).all(),my_all_dep=DepositList.query.filter_by(vc_comp_code=session['comp_code']).order_by(DepositList.nu_account_no).all(),dep_sum_all = db.session.query(func.sum(DepositList.nu_amt).label("sum_amt")).filter_by(vc_comp_code=session['comp_code']).all(),loan_sum_all = db.session.query(func.sum(LoanList.nu_amt).label("sum_amt")).filter_by(vc_cleared_status='NO',vc_comp_code=session['comp_code']).all(),loan_sum = db.session.query(func.sum(LoanList.nu_amt).label("sum_amt")).filter_by(nu_account_no=session['account_no'],vc_cleared_status='NO',vc_comp_code=session['comp_code']).all())

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
				add_data=UserLogin(request.form['account_no'],request.form['reg_date'],request.form['full_name'],request.form['gender'],request.form['contact'],request.form['address'],request.form['password'],request.form['user_type'],request.form['email'],session['comp_code'])
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
				add_data=DepositList(request.form['account_no'],request.form['amt'],request.form['reg_date'],request.form['deposited_by'],request.form['cashier_name'],session['comp_code'])
				db.session.add(add_data)
				db.session.commit()            
				pass
				qry_sum_dep = db.session.query(func.sum(DepositList.nu_amt).label("sum_amt")).filter_by(nu_account_no=session['account_no'],vc_comp_code=session['comp_code']).all()
				my_saving=db.session.query(DepositList).filter_by(nu_account_no=session['account_no'],vc_comp_code=session['comp_code']).order_by(DepositList.dt_date).all()
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
				add_data=LoanList(request.form['account_no'],request.form['amt'],request.form['reg_date'],request.form['loan_desc'],request.form['added_by'],request.form['cashier_name'],request.form['clear_status'],session['comp_code'])
				db.session.add(add_data)
				db.session.commit()            
				pass
				qry_sum_dep = db.session.query(func.sum(DepositList.nu_amt).label("sum_amt")).filter_by(nu_account_no=session['account_no'],vc_comp_code=session['comp_code']).all()
				my_saving=db.session.query(DepositList).filter_by(nu_account_no=session['account_no'],vc_comp_code=session['comp_code']).order_by(DepositList.dt_date).all()
	    		return render_template('home.html', my_var=request.args.get('AddLoan', 'SUCCESS-LOAN'),my_deposit=my_saving,qry_sum_dep=qry_sum_dep)

		except:
			pass
        	return render_template('home.html', my_var=request.args.get('AddLoan', 'LOAN-INVALID_ENTRY'))

@app.route("/UpdateMembers")
def UpdateMembers():

	return render_template('home.html',member_edit=db.session.query(UserLogin).filter_by(nu_account_no=request.args.get('my_var', ''),vc_comp_code=session['comp_code']),my_var=request.args.get('MemberUpdateForm', 'MemberUpdateForm'))

@app.route("/ExecuteUpdateMember",methods=['POST'])
def ExecuteUpdateMember():
	try:
		db.session.query(UserLogin).filter_by(nu_account_no=request.form['update_account_no']).update({UserLogin.nu_account_no:request.form['account_no'],UserLogin.dt_date:request.form['reg_date'],UserLogin.vc_full_name:request.form['full_name'],UserLogin.vc_gender:request.form['gender'],UserLogin.vc_contact:request.form['contact'],UserLogin.vc_address:request.form['address'],UserLogin.vc_pass_word:request.form['password'],UserLogin.user_type:request.form['user_type'],UserLogin.vc_email:request.form['email'],UserLogin.vc_comp_code:session['comp_code']})
		db.session.commit()
		return render_template('home.html',my_member=UserLogin.query.filter_by(vc_comp_code=session['comp_code']).order_by(UserLogin.nu_account_no).all(),my_var=request.args.get('ViewMembers', 'SUCCESS-UPDATE'))
		
	except:
		pass
        return render_template('home.html', my_var=request.args.get('ViewMembers', 'INVALID_UPDATE'))

@app.route("/DeleteMembers")
def DeleteMembers():
	try:
		delete_member=db.session.query(UserLogin).filter_by(nu_account_no=request.args.get('my_var', ''),vc_comp_code=session['comp_code']).first()
		db.session.delete(delete_member)
		db.session.commit()
		return render_template('home.html',my_member=UserLogin.query.filter_by(vc_comp_code=session['comp_code']).order_by(UserLogin.nu_account_no).all(),my_var=request.args.get('ViewMembers', 'SUCCESS-DELETE'))
	except:
		return render_template('home.html', my_var=request.args.get('ViewMembers', 'INVALID_DELETE'))
@app.route("/UpdateDeposit")
def UpdateDeposit():
	return render_template('home.html',deposit_edit=db.session.query(DepositList).filter_by(nu_trans_id=request.args.get('my_var', ''),vc_comp_code=session['comp_code']),my_var=request.args.get('DepositUpdateForm', 'DepositUpdateForm'))

@app.route("/ExecuteUpdateDeposit",methods=['POST'])
def ExecuteUpdateDeposit():
	try:
		db.session.query(DepositList).filter_by(nu_trans_id=request.form['nu_trans_id']).update({DepositList.nu_account_no:request.form['account_no'],DepositList.nu_amt:request.form['amt'],DepositList.dt_date:request.form['reg_date'],DepositList.vc_dep_by:request.form['deposited_by'],DepositList.vc_cashier:request.form['cashier_name'],DepositList.vc_comp_code:session['comp_code']})
		db.session.commit()
		return render_template('home.html',my_all_dep=DepositList.query.filter_by(vc_comp_code=session['comp_code']).order_by(DepositList.nu_account_no).all(),dep_sum_all = db.session.query(func.sum(DepositList.nu_amt).label("sum_amt")).all(),my_var=request.args.get('ViewDeposits', 'SUCCESS-DEPOSIT-UPDATE'))
		
	except:
		pass
        return render_template('home.html', my_var=request.args.get('ViewDeposits', 'INVALID_DEPOSIT_UPDATE'))

@app.route("/DeleteDeposit")
def DeleteDeposit():
	try:
		delete_deposit=db.session.query(DepositList).filter_by(nu_trans_id=request.args.get('my_var', ''),vc_comp_code=session['comp_code']).first()
		db.session.delete(delete_deposit)
		db.session.commit()
		return render_template('home.html',my_all_dep=DepositList.query.filter_by(vc_comp_code=session['comp_code']).order_by(DepositList.nu_account_no).all(),dep_sum_all = db.session.query(func.sum(DepositList.nu_amt).label("sum_amt")).all(),my_var=request.args.get('ViewDeposits', 'SUCCESS-DEPOSIT-DELETE'))
		
	except:
		pass
        return render_template('home.html', my_var=request.args.get('ViewDeposits', 'INVALID_DEPOSIT_DELETE'))
@app.route("/UpdateLoan")
def UpdateLoan():
	return render_template('home.html',loan_edit=db.session.query(LoanList).filter_by(nu_trans_id=request.args.get('my_var', ''),vc_comp_code=session['comp_code']),my_var=request.args.get('LoanUpdateForm', 'LoanUpdateForm'))

@app.route("/ExecuteUpdateLoan",methods=['POST'])
def ExecuteUpdateLoan():
	try:
		db.session.query(LoanList).filter_by(nu_trans_id=request.form['nu_trans_id']).update({LoanList.nu_account_no:request.form['account_no'],LoanList.nu_amt:request.form['amt'],LoanList.dt_date:request.form['reg_date'],LoanList.vc_loan_desc:request.form['loan_desc'],LoanList.vc_added_by:request.form['added_by'],LoanList.vc_cashier:request.form['cashier_name'],LoanList.vc_cleared_status:request.form['clear_status'],LoanList.vc_comp_code:session['comp_code']})
		db.session.commit()
		return render_template('home.html',loan_all=LoanList.query.filter_by(vc_cleared_status='NO',vc_comp_code=session['comp_code']).order_by(LoanList.dt_date).all(),loan_sum_all = db.session.query(func.sum(LoanList.nu_amt).label("sum_amt")).filter_by(vc_cleared_status='NO').all(),my_var=request.args.get('ViewLoan', 'SUCCESS-LOAN-UPDATE'))
		
	except:
		pass
        return render_template('home.html', my_var=request.args.get('ViewLoan', 'INVALID_LOAN_UPDATE'))

@app.route("/DeleteLoan")
def DeleteLoan():
	try:
		delete_loan=db.session.query(LoanList).filter_by(nu_trans_id=request.args.get('my_var', ''),vc_comp_code=session['comp_code']).first()
		db.session.delete(delete_loan)
		db.session.commit()
		return render_template('home.html',loan_all=LoanList.query.filter_by(vc_cleared_status='NO',vc_comp_code=session['comp_code']).order_by(LoanList.dt_date).all(),loan_sum_all = db.session.query(func.sum(LoanList.nu_amt).label("sum_amt")).filter_by(vc_cleared_status='NO').all(),my_var=request.args.get('ViewLoan', 'SUCCESS-LOAN-DELETE'))
	
	except:
		pass
        return render_template('home.html', my_var=request.args.get('ViewLoan', 'INVALID_LOAN_DELETE'))

@app.route("/UpdatePassword",methods=['POST'])
def UpdatePassword():
	if request.form['password']=='' or request.form['comfirm_password']=='':
		return render_template('home.html', my_var=request.args.get('ChangePassword','PASSWORD-EMPTY_FIELDS'))
	else:
		if request.form['password'] !=request.form['comfirm_password']:

			return render_template('home.html', my_var=request.args.get('ChangePassword','PASSWORD-EXISTS'))
		else:	
			try:

				db.session.query(UserLogin).filter_by(nu_account_no=session['account_no'],vc_comp_code=session['comp_code']).update({UserLogin.vc_pass_word:request.form['password']})
				db.session.commit()
				qry_sum_dep = db.session.query(func.sum(DepositList.nu_amt).label("sum_amt")).filter_by(nu_account_no=session['account_no'],vc_comp_code=session['comp_code']).all()
				my_saving=db.session.query(DepositList).filter_by(nu_account_no=session['account_no'],vc_comp_code=session['comp_code']).order_by(DepositList.dt_date).all()
				#----------------------COMP_INFO.................................
				return render_template('home.html',my_deposit=my_saving,qry_sum_dep=qry_sum_dep)
			except:
				pass
				return render_template('home.html', my_var=request.args.get('ChangePassword', 'PASSWORD-INVALID_ENTRY'))
@app.route("/UpdateCompanyInfo",methods=['POST'])
def UpdateCompanyInfo():
	if request.form['comp_name']=='' or request.form['comp_abrev']=='':
		return render_template('home.html', my_var=request.args.get('CompanyInfo','COMPNAY-EMPTY_FIELDS'))
	else:
		try:
			db.session.query(CompInfo).filter_by(vc_comp_code=session['comp_code']).update({CompInfo.vc_comp_name:request.form['comp_name'],CompInfo.vc_comp_address:request.form['comp_address'],CompInfo.vc_comp_abrev:request.form['comp_abrev'],CompInfo.vc_comp_slogan:request.form['comp_slogan'],CompInfo.vc_comp_contact:request.form['comp_contact'],CompInfo.vc_email:request.form['comp_email'],CompInfo.vc_website:request.form['comp_website']})
			db.session.commit()
			session['logged_in'] = False
			return home()
		except:
			pass
			return render_template('home.html', my_var=request.args.get('CompanyInfo', 'COMPANY-INVALID_ENTRY'))				

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='0.0.0.0', port=4000)
