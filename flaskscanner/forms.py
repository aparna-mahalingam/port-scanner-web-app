from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField
from wtforms.validators import DataRequired, InputRequired, IPAddress, Length, EqualTo
import logging



class ScannerInputForm(FlaskForm):
	target_ipAddr = StringField('Target IPv4 Address / Hostname',
							validators=[InputRequired()] )
	submit = SubmitField('Scan')


class HistoryOfAnIP(FlaskForm):
	"""
	Additional feature that might be useful:
	To query database to check history of past scans for a particular IP Address
	Does not perform any active scanning; only returns details of previous scans
	"""
	ipAddr_to_query = StringField('IP Address',
							validators=[ DataRequired(), InputRequired(),
							IPAddress(ipv4=True, ipv6=False, message="Please Enter Valid IPv4 Address, e.g. 10.0.0.10")] )
	submit = SubmitField('Check History')
