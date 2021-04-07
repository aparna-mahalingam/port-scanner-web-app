import re, socket
import logging



def validate_ip_hostname(ipOrHostname):
	"""
	Custom validation for input -- check if IP Address or hostname, and then validate further
	"""
	if not re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", ipOrHostname):
		try:
			socket.gethostbyname(ipOrHostname)
		except Exception as e:
			logging.debug("Invalid hostname provided.")
			return(False)
	else:
		# validate IP Address thoroughly
		ip_check = "^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$"
		if not re.search(ip_check, ipOrHostname):
			logging.debug("Invalid IP Address provided.")
			return(False)
	return(True)