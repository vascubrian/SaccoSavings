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
    def __init__(self,nu_account_no,dt_date,vc_full_name,vc_gender,vc_contact,vc_address,vc_pass_word,user_type):
        self.nu_account_no=nu_account_no
        self.dt_date=dt_date
        self.vc_full_name=vc_full_name
        self.vc_gender=vc_gender
        self.vc_contact=vc_contact
        self.vc_address=vc_address
        self.vc_pass_word=vc_pass_word
        self.user_type=user_type




	



