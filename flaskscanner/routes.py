from flask import render_template, url_for, flash, request, redirect
from flaskscanner.db_models import IPScanDetails
from flaskscanner.port_scanner import scan_ports_on_host
from flaskscanner.forms import ScannerInputForm, HistoryOfAnIP
from flaskscanner import app, db
from datetime import datetime
from flaskscanner.port_state_change_and_history import get_past_scans, get_port_state_change
from flaskscanner.ip_validator import validate_ip_hostname
import socket
import logging



@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
@app.route('/scan', methods=['GET', 'POST'])
def scanner_home_page():
	headings = ("Date & Time of Scan", "Open Ports on IP")

	form = ScannerInputForm()

	if form.validate_on_submit():	
		logging.debug(f"User entered: {form.target_ipAddr.data}")	

		if validate_ip_hostname(form.target_ipAddr.data):
			# database will store hostnames translated into IPs
			target_ip = socket.gethostbyname(form.target_ipAddr.data)
			logging.debug(f"Translated IP: {target_ip}")

			# perform port scanning and get changes since previous scan
			openports = set(scan_ports_on_host(target_ip) )
			openports_str = ', '.join(str(port) for port in openports)
			timestamp = datetime.now()
			timestamp_str = timestamp.strftime("%b-%d-%Y, %-I:%M:%S %p")

			# first obtain previous scan result before updating records with new scan
			data = tuple(get_past_scans(target_ip) )
			if data:
				closed_ports, newly_opened_ports = get_port_state_change(target_ip, openports_str)

			# commit to db
			scanned_ip = IPScanDetails(ip_address=target_ip, open_ports=openports_str, timestamp=timestamp)
			logging.debug(f"Updating new scan record in DB: {scanned_ip}")
			db.session.add(scanned_ip)
			db.session.commit()
			
			flash(f"Successfully scanned '{form.target_ipAddr.data}' for open ports.", 'success')
			return render_template('scan_results.html', **locals() )
		else:
			flash("Invalid IP/Hostname provided! Please try again.", 'warning')
	return render_template('scanner_home.html', title='Port Scanner', form=form)


@app.route('/scan-history-check', methods=['GET', 'POST'])
def history_page():
	headings = ("Date & Time of Scan", "Open Ports on IP")

	form = HistoryOfAnIP()
	
	num_scans_done_on_ip = 0

	if form.validate_on_submit():
		# user wishes only for scan history for an ip, without having to scan 
		scans_history_for_ip = get_past_scans(form.ipAddr_to_query.data)

		num_scans_done_on_ip = len(scans_history_for_ip)
		if scans_history_for_ip:
			if num_scans_done_on_ip == 1:
				flash(f'Host {form.ipAddr_to_query.data} has been scanned once!', 'success')
			else:
				flash(f'Host {form.ipAddr_to_query.data} has been scanned {num_scans_done_on_ip} times!', 'success')
		else:
			flash(f'This IP has never been scanned!', 'warning')
	return render_template('scan_history.html', title='Scan Check for IP', **locals() )

