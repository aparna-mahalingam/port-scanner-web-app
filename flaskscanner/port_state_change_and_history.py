from datetime import datetime
from flaskscanner import app, db
from flaskscanner.db_models import IPScanDetails
import logging



def get_past_scans(ip_address):
	"""
	Obtains the history of all the scans performed on a given IP Address by querying the db
	Returns: list of tuples [ (str(date): openports) ]
	"""
	past_scans = IPScanDetails.query.filter_by(ip_address=ip_address).all()
	if not past_scans:
		logging.debug(f"IP {ip_address} has no previous scans")

	ip_scan_history = []

	for past_scan in past_scans:
		# convert datetime object to string readable format
		datetime_of_scan = past_scan.timestamp.strftime("%b-%d-%Y, %-I:%M:%S %p")
		openports = past_scan.open_ports
		ip_scan_history.append( (datetime_of_scan, openports) )
	return(ip_scan_history)


def get_port_state_change(ip_address, openports):
	"""
	Returns: list of ports that have changed (CLOSED / OPENED) since the previous scan
	"""
	# query result ordered by timestamp in ascending
	previous_scan = IPScanDetails.query.filter_by(ip_address=ip_address).order_by(IPScanDetails.timestamp).all()[-1]

	previously_open_ports = previous_scan.open_ports.split(', ')
	currently_open_ports = openports.split(', ')

	logging.debug(f"Changed ports --> now= {currently_open_ports}, previous= {previously_open_ports}")
	
	if currently_open_ports == previously_open_ports:
		logging.debug(f"Changed ports: none!")
		return('0', '0')

	closed = set(previously_open_ports) - set(currently_open_ports)
	closed_ports = [[i, 'CLOSED'] for i in closed]
	newly_opened =  set(currently_open_ports) - set(previously_open_ports)
	newly_opened_ports =[[i, 'OPENED'] for i in newly_opened]

	return(closed_ports, newly_opened_ports)
