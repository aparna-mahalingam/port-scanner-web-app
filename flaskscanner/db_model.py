from datetime import datetime
from flaskscanner import db
import logging



class IPScanDetails(db.Model):
	__tablename__ = 'ip_scan_details'
	ip_address = db.Column(db.String(20), primary_key=True, nullable=False)
	timestamp = db.Column(db.DateTime, primary_key=True, nullable=False, default=datetime.now)

	open_ports = db.Column(db.Text, nullable=False)

	def __repr__(self):
		return f"ScanResult('{self.ip_address}', '{self.timestamp}', '{self.open_ports}')"
