from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

class BaseModel(db.Model):
    """Base data model for all objects"""
    __abstract__ = True

    def __init__(self, *args):
        super().__init__(*args)

    # def __repr__(self):
    #     """Define a base way to print models"""
    #     return '%s(%s)' % (self.__class__.__name__, {
    #         column: value
    #         for column, value in self._to_dict().items()
    #     })

    def json(self):
        """
                Define a base way to jsonify models, dealing with datetime objects
        """
        return {
            column: value if not isinstance(value, datetime.date) else value.strftime('%Y-%m-%d')
            for column, value in self._to_dict().items()
        }


class UserLogin(BaseModel, db.Model):
    """Model for the mst_logn table"""
    __tablename__ = 'mst_login'

    nu_account_no = db.Column("nu_account_no",db.Integer,primary_key = True)
    dt_date = db.Column(db.DateTime)
    vc_full_name = db.Column(db.String)
    vc_gender = db.Column(db.String)
    vc_contact = db.Column(db.String)
    vc_address = db.Column(db.String)
    vc_pass_word=db.Column(db.String)
    user_type = db.Column(db.String)
    vc_email = db.Column(db.String)
    def __init__(self,nu_account_no,dt_date,vc_full_name,vc_gender,vc_contact,vc_address,vc_pass_word,user_type,vc_email):
        self.nu_account_no=nu_account_no
        self.dt_date=dt_date
        self.vc_full_name=vc_full_name
        self.vc_gender=vc_gender
        self.vc_contact=vc_contact
        self.vc_address=vc_address
        self.vc_pass_word=vc_pass_word
        self.user_type=user_type
        self.vc_email=vc_email

class DepositList(BaseModel,db.Model):
    __tablename__ ='dt_deposit'

    nu_trans_id = db.Column("nu_trans_id",db.Integer,primary_key = True)
    nu_account_no = db.Column(db.Integer)
    nu_amt = db.Column(db.Integer)
    dt_date = db.Column(db.DateTime)
    vc_dep_by = db.Column(db.String)
    vc_cashier = db.Column(db.String)
    def __init__(self,nu_account_no,nu_amt,dt_date,vc_dep_by,vc_cashier):
        self.nu_account_no=nu_account_no
        self.nu_amt=nu_amt
        self.dt_date=dt_date
        self.vc_dep_by=vc_dep_by
        self.vc_cashier=vc_cashier
class LoanList(BaseModel,db.Model):
    """docstring for LoanList"""
    __tablename__ ='dt_loan'
    nu_trans_id = db.Column("nu_trans_id",db.Integer,primary_key = True)
    nu_account_no=db.Column(db.Integer)
    nu_amt=db.Column(db.Integer)
    dt_date=db.Column(db.DateTime)
    vc_loan_desc=db.Column(db.String)
    vc_added_by=db.Column(db.String)
    vc_cashier=db.Column(db.String)
    vc_cleared_status=db.Column(db.String)

    def __init__(self,nu_account_no,nu_amt,dt_date,vc_loan_desc,vc_added_by,vc_cashier,vc_cleared_status):
        self.nu_account_no =nu_account_no
        self.nu_amt=nu_amt
        self.dt_date=dt_date
        self.vc_loan_desc=vc_loan_desc
        self.vc_added_by=vc_added_by
        self.vc_cashier=vc_cashier
        self.vc_cleared_status=vc_cleared_status        





	



